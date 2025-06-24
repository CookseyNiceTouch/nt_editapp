import logging
import sys
import os
import json # Added for reading JSON file

# Setup basic logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ResolveAPI:
    def __init__(self):
        logger.debug('Initializing ResolveAPI instance...')
        try:
            # Add the lib directory to the Python path for DaVinci Resolve imports
            current_dir = os.path.dirname(os.path.abspath(__file__))
            lib_dir = os.path.join(current_dir, 'lib')
            if lib_dir not in sys.path:
                sys.path.insert(0, lib_dir)
            
            import DaVinciResolveScript as dvr_script
        except ImportError as e:
            logger.error('Could not import DaVinciResolveScript: %s', e)
            logger.error('Make sure DaVinci Resolve is installed and the fusionscript.dll is in the lib directory')
            raise
        self.dvr_script = dvr_script # Store for later use
        
        # Try to get resolve object
        try:
            self.resolve = dvr_script.scriptapp('Resolve')
            if not self.resolve:
                logger.error('Could not connect to DaVinci Resolve instance. Make sure:')
                logger.error('1. DaVinci Resolve is running')
                logger.error('2. "External scripting using" is enabled in Resolve preferences')
                logger.error('3. The correct scripting mode (Local/Network) is selected')
                raise RuntimeError('Could not connect to DaVinci Resolve instance.')
            logger.debug('Connected to DaVinci Resolve instance.')
        except Exception as e:
            logger.error('Failed to connect to DaVinci Resolve: %s', e)
            logger.error('Troubleshooting tips:')
            logger.error('- Ensure DaVinci Resolve is running')
            logger.error('- Check that external scripting is enabled in Resolve > Preferences > General')
            logger.error('- Verify the scripting connection mode matches your setup')
            raise
        
        # Get project manager
        try:
            self.project_manager = self.resolve.GetProjectManager()
            if not self.project_manager:
                raise RuntimeError('Could not get ProjectManager from Resolve.')
            logger.debug('ProjectManager acquired.')
        except Exception as e:
            logger.error('Failed to get ProjectManager: %s', e)
            raise

    def list_projects(self):
        logger.debug('Retrieving list of projects...')
        try:
            # Get dict of project names in the current folder
            project_dict = self.project_manager.GetProjectsInCurrentFolder()
            logger.debug('Projects found (dict): %s', project_dict)
            project_names = list(project_dict.values()) if project_dict else []
            logger.debug('Project names list: %s', project_names)
            return project_names
        except Exception as e:
            logger.error('Error retrieving project list: %s', e)
            return None 

    def create_project(self, project_name):
        logger.debug('Creating new project: %s', project_name)
        try:
            project = self.project_manager.CreateProject(project_name)
            if project:
                logger.debug('Project created successfully: %s', project_name)
                # Log project details
                logger.debug('Project details: %s', dir(project))
                # Refresh project manager to update the list
                self.project_manager = self.resolve.GetProjectManager()
            else:
                logger.warning('Project creation failed: %s', project_name)
            return project
        except Exception as e:
            logger.error('Error creating project: %s', e)
            return None

    def create_timeline(self, project, timeline_name="Timeline 1"):
        """Create a new timeline in the specified project."""
        logger.debug('Creating new timeline: %s in project', timeline_name)
        try:
            if not project:
                logger.error('No project provided for timeline creation')
                return None
            
            # Get the project's media pool
            media_pool = project.GetMediaPool()
            if not media_pool:
                logger.error('Could not get media pool from project')
                return None
            
            # Create a new empty timeline
            timeline = media_pool.CreateEmptyTimeline(timeline_name)
            if timeline:
                logger.debug('Timeline created successfully: %s', timeline_name)
                logger.debug('Timeline details: %s', dir(timeline))
            else:
                logger.warning('Timeline creation failed: %s', timeline_name)
            return timeline
        except Exception as e:
            logger.error('Error creating timeline: %s', e)
            return None 

    def get_media_pool_item_unique_id(self, nt_project_json_path, target_clip_name):
        logger.debug(f"Attempting to get Unique ID for clip '{target_clip_name}' using JSON '{nt_project_json_path}'")
        try:
            if not os.path.exists(nt_project_json_path):
                logger.error(f"Nice Touch JSON file not found: {nt_project_json_path}")
                return None
            
            with open(nt_project_json_path, 'r') as f:
                nt_project_data = json.load(f)
            
            resolve_project_name = nt_project_data.get("resolve_project_name")
            if not resolve_project_name:
                logger.error("'resolve_project_name' not found in the JSON file.")
                return None
            logger.info(f"Target Resolve project name from JSON: {resolve_project_name}")

            project = self.project_manager.LoadProject(resolve_project_name)
            if not project:
                current_project = self.project_manager.GetCurrentProject()
                if current_project and current_project.GetName() == resolve_project_name:
                    logger.info(f"Project '{resolve_project_name}' is already the current project.")
                    project = current_project
                else:
                    logger.error(f"Could not load or find project '{resolve_project_name}'.")
                    return None
            
            logger.info(f"Successfully accessed project: {project.GetName()}")

            media_pool = project.GetMediaPool()
            if not media_pool:
                logger.error("Could not get Media Pool for the project.")
                return None

            root_folder = media_pool.GetRootFolder()
            if not root_folder:
                logger.error("Could not get root folder from Media Pool.")
                return None
            
            clips_list = root_folder.GetClipList()
            if not clips_list:
                logger.warning(f"No clips found in the root folder for project '{project.GetName()}'.")
                return None

            for media_pool_item in clips_list:
                if media_pool_item.GetName() == target_clip_name:
                    logger.info(f"Found matching clip: {target_clip_name}")
                    unique_id = media_pool_item.GetUniqueId()
                    logger.info(f"Retrieved Unique ID: {unique_id}")
                    return unique_id
            
            logger.warning(f"Clip '{target_clip_name}' not found in Media Pool for project '{project.GetName()}'.")
            return None

        except Exception as e:
            logger.error(f"Error in get_media_pool_item_unique_id: {e}", exc_info=True)
            return None 

    def prepare_clips_for_timeline(self, nt_project_json_path):
        # This method will be removed and its logic incorporated into the new one.
        pass

    def add_clips_to_timeline_from_json(self, nt_project_json_path):
        logger.info(f"Attempting to add clips to timeline from JSON: {nt_project_json_path}")
        project_uuid_for_log = "N/A"
        timeline_uuid_for_log = "N/A"
        try:
            # 1. Read JSON
            if not os.path.exists(nt_project_json_path):
                logger.error(f"Nice Touch JSON file not found: {nt_project_json_path}")
                return False
            with open(nt_project_json_path, 'r') as f:
                nt_project_data = json.load(f)

            resolve_project_name = nt_project_data.get("resolve_project_name")
            # Assuming resolve_timeline_name exists or will be added to JSON for identifying/creating the timeline
            clips_in_json = nt_project_data.get("clips")

            if not resolve_project_name:
                logger.error("'resolve_project_name' not found in JSON.")
                return False
            if not isinstance(clips_in_json, list):
                logger.error("'clips' array not found or not a list in JSON.")
                return False

            # 2. Load Project & Get its UUID
            logger.debug(f"Loading Resolve project: {resolve_project_name}")
            project = self.project_manager.LoadProject(resolve_project_name)
            if not project:
                current_project_check = self.project_manager.GetCurrentProject()
                if current_project_check and current_project_check.GetName() == resolve_project_name:
                    project = current_project_check
                    logger.info(f"Project '{resolve_project_name}' is already current.")
                else:
                    logger.error(f"Failed to load or find project: {resolve_project_name}")
                    return False
            project_uuid_for_log = project.GetUniqueId()
            logger.info(f"Accessed project '{project.GetName()}' with UUID: {project_uuid_for_log}")
            media_pool = project.GetMediaPool()

            # 3. Get/Create Timeline & Get its UUID
            resolve_timeline_uuid_from_json = nt_project_data.get("resolve_timeline_uuid")
            resolve_timeline_name_from_json = nt_project_data.get("resolve_timeline_name", "Timeline from NiceTouch") # Default name if not in JSON
            timeline = None

            if resolve_timeline_uuid_from_json and isinstance(resolve_timeline_uuid_from_json, str) and resolve_timeline_uuid_from_json.strip() != "":
                logger.info(f"Attempting to find timeline by UUID: {resolve_timeline_uuid_from_json}")
                timeline_count = project.GetTimelineCount()
                if timeline_count > 0:
                    for i in range(1, timeline_count + 1):
                        timeline_by_index = project.GetTimelineByIndex(i)
                        if timeline_by_index and timeline_by_index.GetUniqueId() == resolve_timeline_uuid_from_json:
                            timeline = timeline_by_index
                            logger.info(f"Found timeline '{timeline.GetName()}' by UUID: {resolve_timeline_uuid_from_json}")
                            break
                if not timeline:
                    logger.error(f"Timeline with UUID '{resolve_timeline_uuid_from_json}' not found in project. Aborting, as a specific UUID was provided.")
                    return False
            else:
                # UUID is missing, empty, or not a valid string to search for. Create a new timeline.
                logger.info(f"resolve_timeline_uuid is missing, empty, or invalid. Creating new timeline named '{resolve_timeline_name_from_json}'.") 
                if not media_pool:
                    logger.error("Could not get Media Pool to create a new timeline.")
                    return False
                timeline = media_pool.CreateEmptyTimeline(resolve_timeline_name_from_json)
                if not timeline:
                    logger.error(f"Failed to create new timeline named '{resolve_timeline_name_from_json}'.")
                    return False
                logger.info(f"Created new timeline: '{timeline.GetName()}'")
                
                # Get UUID of newly created timeline and update the JSON file
                newly_created_timeline_uuid = timeline.GetUniqueId()
                if newly_created_timeline_uuid:
                    logger.info(f"New timeline has UUID: {newly_created_timeline_uuid}. Attempting to update JSON file.")
                    nt_project_data["resolve_timeline_uuid"] = newly_created_timeline_uuid # Update the loaded data
                    try:
                        with open(nt_project_json_path, 'w') as f_write:
                            json.dump(nt_project_data, f_write, indent=4)
                        logger.info(f"Successfully updated JSON file '{nt_project_json_path}' with new timeline UUID: {newly_created_timeline_uuid}")
                    except Exception as json_write_e:
                        logger.error(f"Failed to write updated timeline UUID back to JSON file '{nt_project_json_path}': {json_write_e}")
                        # Continue with the operation even if JSON update fails, but log it clearly.
                else:
                    logger.warning("Could not get UUID for the newly created timeline. JSON file will not be updated with timeline UUID.")
            
            if not timeline: # Safeguard, should be caught by earlier returns
                logger.error("Failed to identify or create a timeline. Aborting.")
                return False

            project.SetCurrentTimeline(timeline)
            timeline_uuid_for_log = timeline.GetUniqueId()
            logger.info(f"Using timeline '{timeline.GetName()}' with UUID: {timeline_uuid_for_log}")

            # 4. Prepare clipInfo List (Resolving MediaPoolItem names to objects)
            clip_infos_for_api = []
            root_folder = media_pool.GetRootFolder()
            if not root_folder:
                logger.error("Could not get root folder from Media Pool.")
                return False
            media_pool_clips_list = root_folder.GetClipList()
            if not media_pool_clips_list:
                logger.warning("Media pool root folder is empty.")
                # No clips to process from media pool, so can't match JSON clips

            for clip_entry in clips_in_json:
                mpi_uuid_from_json = clip_entry.get("mediapool_item_uuid")
                start_frame = clip_entry.get("start_frame")
                end_frame = clip_entry.get("end_frame")

                if not mpi_uuid_from_json or start_frame is None or end_frame is None:
                    logger.warning(f"Skipping JSON clip entry due to missing name, start, or end frame: {clip_entry}")
                    continue
                
                found_mpi_object = None
                if media_pool_clips_list: # Only search if there are clips in the media pool
                    for mpi_object_in_pool in media_pool_clips_list:
                        if mpi_object_in_pool.GetUniqueId() == mpi_uuid_from_json:
                            found_mpi_object = mpi_object_in_pool
                            break
                
                if found_mpi_object:
                    clip_info = {
                        "mediaPoolItem": found_mpi_object,
                        "startFrame": int(start_frame),
                        "endFrame": int(end_frame),
                        "position_id": clip_entry.get("position_id")
                    }
                    clip_infos_for_api.append(clip_info)
                    logger.debug(f"Prepared API clip info for: {mpi_uuid_from_json}")
                else:
                    logger.warning(f"MediaPoolItem with UUID '{mpi_uuid_from_json}' not found in Media Pool. Skipping.")

            # Sort clip_infos_for_api by nt_position_id before appending
            if clip_infos_for_api:
                logger.debug(f"Original prepared clips order: {clip_infos_for_api}")
                try:
                    # Ensure nt_position_id is present and can be used for sorting, provide a default if missing for robustness
                    clip_infos_for_api.sort(key=lambda x: x.get('position_id', float('inf')))
                    logger.info(f"Sorted clip infos by 'position_id' for timeline append: {clip_infos_for_api}")
                except TypeError as sort_e:
                    logger.error(f"Could not sort clips by 'position_id' due to incompatible types or missing key. Appending in original order. Error: {sort_e}")
            
            # 5. Append Clips to Timeline
            if not clip_infos_for_api:
                logger.warning("No valid clip infos prepared to add to timeline. Check JSON and Media Pool content.")
                # Consider this a success if no clips were meant to be added, or failure if clips were expected.
                # For now, if clip_infos_for_api is empty but no prior errors, it implies no valid clips from JSON matched.
                return True # Or False, depending on desired behavior for empty valid clip list

            logger.info(f"Attempting to append {len(clip_infos_for_api)} clips to timeline '{timeline.GetName()}'")
            append_success = media_pool.AppendToTimeline(clip_infos_for_api)

            if append_success:
                logger.info(f"Successfully appended {len(clip_infos_for_api)} clips to timeline.")
                logger.info(f"Project UUID: {project_uuid_for_log}, Timeline UUID: {timeline_uuid_for_log}")
                return True
            else:
                logger.error(f"Failed to append clips to timeline. Resolve API returned failure.")
                logger.info(f"Project UUID: {project_uuid_for_log}, Timeline UUID: {timeline_uuid_for_log}")
                return False

        except Exception as e:
            logger.error(f"Error in add_clips_to_timeline_from_json: {e}", exc_info=True)
            logger.error(f"Operation state: Project UUID: {project_uuid_for_log}, Timeline UUID: {timeline_uuid_for_log}")
            return False 

    # Method to find timeline by name, returns timeline object or None
    def _find_timeline_by_name(self, project, timeline_name):
        logger.debug(f"Searching for timeline '{timeline_name}' in project '{project.GetName()}'")
        timeline_count = project.GetTimelineCount()
        if timeline_count > 0:
            for i in range(1, timeline_count + 1):
                timeline_obj = project.GetTimelineByIndex(i)
                if timeline_obj and timeline_obj.GetName() == timeline_name:
                    logger.info(f"Found existing timeline '{timeline_name}'")
                    return timeline_obj
        logger.info(f"Timeline '{timeline_name}' not found.")
        return None

    def build_timeline_from_edited_output(self, edited_output_json_path, timeline_name_to_use="Nice Touch Timeline"):
        logger.info(f"Attempting to build timeline '{timeline_name_to_use}' from edited output JSON: {edited_output_json_path}")
        project_uuid_for_log = "N/A"
        timeline_uuid_for_log = "N/A"
        # timeline_name_to_use = "Nice Touch Timeline" # Parameterized now

        try:
            # 1. Get Current Project
            project = self.project_manager.GetCurrentProject()
            if not project:
                logger.error("No project is currently open in DaVinci Resolve.")
                return False # Indicates an error or inability to proceed
            project_uuid_for_log = project.GetUniqueId()
            logger.info(f"Operating on current project: '{project.GetName()}' with UUID: {project_uuid_for_log}")

            media_pool = project.GetMediaPool()
            if not media_pool:
                logger.error("Could not get Media Pool for the current project.")
                return False

            # 2. Handle Timeline
            timeline = self._find_timeline_by_name(project, timeline_name_to_use)

            if timeline:
                logger.info(f"Found existing timeline: '{timeline.GetName()}' (UUID: {timeline.GetUniqueId()}). Clearing existing clips from track 1 (video & audio).")
                project.SetCurrentTimeline(timeline) # Ensure it's the current timeline before modifying
                
                all_clips_to_delete = []
                # Get clips from the first video track
                video_clips_on_track_1 = timeline.GetItemListInTrack("video", 1) 
                if video_clips_on_track_1:
                    logger.debug(f"Found {len(video_clips_on_track_1)} video clips on track 1.")
                    all_clips_to_delete.extend(video_clips_on_track_1)
                else:
                    logger.debug("No video clips found on track 1.")

                # Get clips from the first audio track
                audio_clips_on_track_1 = timeline.GetItemListInTrack("audio", 1)
                if audio_clips_on_track_1:
                    logger.debug(f"Found {len(audio_clips_on_track_1)} audio clips on track 1.")
                    all_clips_to_delete.extend(audio_clips_on_track_1)
                else:
                    logger.debug("No audio clips found on track 1.")
                
                if all_clips_to_delete:
                    logger.info(f"Attempting to delete {len(all_clips_to_delete)} total clips (video and audio) from track 1 of timeline '{timeline.GetName()}'.")
                    delete_success = timeline.DeleteClips(all_clips_to_delete) 
                    if delete_success:
                        logger.info(f"Successfully deleted {len(all_clips_to_delete)} clips from timeline '{timeline.GetName()}'.")
                    else:
                        logger.error(f"Failed to delete clips from timeline '{timeline.GetName()}'. Proceeding to add new clips might result in duplicates or errors.")
                        # Potentially return False here if it's critical that old clips are removed
                else:
                    logger.info(f"No clips found on video track 1 or audio track 1 of timeline '{timeline.GetName()}' to delete.")
            else:
                logger.info(f"Timeline '{timeline_name_to_use}' not found. Creating new timeline.")
                timeline = media_pool.CreateEmptyTimeline(timeline_name_to_use)
                if not timeline:
                    logger.error(f"Failed to create new timeline '{timeline_name_to_use}'.")
                    return False
                project.SetCurrentTimeline(timeline)
                logger.info(f"Successfully created and set current timeline '{timeline.GetName()}'")
            
            timeline_uuid_for_log = timeline.GetUniqueId()
            logger.info(f"Using timeline '{timeline.GetName()}' with UUID: {timeline_uuid_for_log}")

            # 3. Read edited_output.json
            if not os.path.exists(edited_output_json_path):
                logger.error(f"Edited output JSON file not found: {edited_output_json_path}")
                return False
            with open(edited_output_json_path, 'r') as f:
                edited_data = json.load(f)
            
            master_clip_filename = edited_data.get("file_name")
            segments_from_json = edited_data.get("segments") # Renamed to avoid conflict with python 'segments' module if imported elsewhere by mistake

            if not master_clip_filename:
                logger.error("'file_name' not found in edited output JSON.")
                return False
            if not isinstance(segments_from_json, list):
                logger.error("'segments' array not found or not a list in edited output JSON.")
                return False

            # 4. Find the Master MediaPoolItem by name
            root_folder = media_pool.GetRootFolder()
            if not root_folder:
                logger.error("Could not get root folder from Media Pool.")
                return False
            media_pool_clips_list = root_folder.GetClipList() # Corrected to GetClipList
            master_mpi_object = None
            if media_pool_clips_list:
                for mpi in media_pool_clips_list:
                    if mpi.GetName() == master_clip_filename:
                        master_mpi_object = mpi
                        logger.info(f"Found master MediaPoolItem: '{master_clip_filename}' (UUID: {master_mpi_object.GetUniqueId()})")
                        break
            
            if not master_mpi_object:
                logger.error(f"Master clip '{master_clip_filename}' not found in the Media Pool of project '{project.GetName()}'.")
                return False

            # 5. Prepare clipInfo Dictionaries from Segments
            clip_infos_for_api = []
            for seg in segments_from_json:
                frame_in = seg.get("frame_in")
                frame_out = seg.get("frame_out")
                clip_order = seg.get("clip_order") 

                if frame_in is None or frame_out is None or clip_order is None:
                    logger.warning(f"Skipping segment due to missing frame_in, frame_out, or clip_order: {seg.get('segment_id', '(no id)')}")
                    continue
                
                clip_info = {
                    "mediaPoolItem": master_mpi_object, 
                    "startFrame": int(frame_in),
                    "endFrame": int(frame_out),
                    "source_clip_order": clip_order 
                }
                clip_infos_for_api.append(clip_info)
            
            if not clip_infos_for_api:
                logger.warning("No valid segments found in JSON to add to timeline.")
                return True 

            # 6. Sort by source_clip_order
            logger.debug(f"Unsorted clip infos (from segments): {clip_infos_for_api}")
            try:
                clip_infos_for_api.sort(key=lambda x: x.get('source_clip_order', float('inf')))
                logger.info(f"Sorted clip infos for timeline append: {clip_infos_for_api}")
            except TypeError as sort_e:
                logger.error(f"Could not sort clips by 'source_clip_order'. Appending in original order. Error: {sort_e}")

            # 7. Append to Timeline
            logger.info(f"Attempting to append {len(clip_infos_for_api)} segments to timeline '{timeline.GetName()}'")
            append_success = media_pool.AppendToTimeline(clip_infos_for_api)

            if append_success:
                logger.info(f"Successfully appended {len(clip_infos_for_api)} segments to timeline.")
                logger.info(f"Project UUID: {project_uuid_for_log}, Timeline UUID: {timeline_uuid_for_log}")
                return True
            else:
                logger.error(f"Failed to append segments to timeline. Resolve API returned failure.")
                logger.info(f"Project UUID: {project_uuid_for_log}, Timeline UUID: {timeline_uuid_for_log}")
                return False

        except Exception as e:
            logger.error(f"Error in build_timeline_from_edited_output: {e}", exc_info=True)
            logger.error(f"Operation state: Project UUID: {project_uuid_for_log}, Timeline UUID: {timeline_uuid_for_log}")
            return False # General error 

    def export_timeline_as_aaf(self, timeline_name="Nice Touch Timeline", output_dir="data/exports"):
        logger.info(f"Attempting to export timeline '{timeline_name}' as AAF to directory '{output_dir}'")
        project = self.project_manager.GetCurrentProject()
        if not project:
            logger.error("No project is currently open in DaVinci Resolve.")
            return False

        timeline = self._find_timeline_by_name(project, timeline_name)
        if not timeline:
            logger.error(f"Timeline '{timeline_name}' not found in project '{project.GetName()}'.")
            return False

        # Ensure output directory exists
        if not os.path.isabs(output_dir):
            output_dir = os.path.abspath(output_dir)
        os.makedirs(output_dir, exist_ok=True)

        # Define AAF export settings
        # Based on Resolve scripting documentation, ExportTimeline takes these parameters:
        # timeline (Timeline object): The timeline to export.
        # filePath (string): The full path to the output file (including filename and extension).
        # exportType (int): self.dvr_script.EXPORT_AAF, self.dvr_script.EXPORT_DRT, etc.
        # exportSubtype (int): e.g., self.dvr_script.EXPORT_AAF_NEW, self.dvr_script.EXPORT_AAF_EXISTING_WITH_NEW_VERSION
        # Example settings for a new AAF, more options might be available
        # For AAF, we might need to specify additional options like embedded audio, video format, etc.
        # The API might also have specific constants for AAF export. Let's assume a general AAF export for now.
        # The DaVinciResolveScript documentation for ExportTimeline says:
        # bool ExportTimeline(timeline, filePath, exportType<, exportSubtype>)        
        # exportType = dvr_script.EXPORT_AAF, EXPORT_DRT, EXPORT_XML, EXPORT_EDL, EXPORT_TEXT_CSV, EXPORT_TEXT_TAB, EXPORT_IO
        # For AAF export, exportSubtype may not be strictly necessary or could default.
        # Let's try with the basic AAF export type.

        # Sanitize timeline name for use in filename
        safe_timeline_name = "".join(c if c.isalnum() else "_" for c in timeline_name)
        output_filename = f"{safe_timeline_name}.aaf"
        output_filepath = os.path.join(output_dir, output_filename)

        logger.info(f"Exporting timeline '{timeline_name}' to '{output_filepath}'")

        try:
            # EXPORT_AAF = 0 (from typical observations, but should use dvr_script constant)
            # Let's assume dvr_script.EXPORT_AAF exists. If not, we might need to find the correct value.
            # Checking common dvr_script structure:
            # dvr_script.EXPORT_AAF = 0
            # dvr_script.EXPORT_DRT = 1
            # dvr_script.EXPORT_XML = 2
            # dvr_script.EXPORT_EDL = 3
            # etc.
            # For now, let's directly use the assumed constant name. The DaVinciResolveScript module
            # should define these.
            export_type_aaf = getattr(self.dvr_script, 'EXPORT_AAF', None)
            if export_type_aaf is None:
                logger.error("DaVinciResolveScript.EXPORT_AAF constant not found. Cannot export AAF.")
                logger.warning("Attempting to use integer value 0 for EXPORT_AAF as a fallback. This may not work.")
                export_type_aaf = 0 # Fallback, highly risky.
            
            # Regarding exportSubtype: For AAF, it seems it might not always be needed or has defaults.
            # Some documentation hints at constants like AAF_EMBEDDED_AUDIO or AAF_LINK_TO_SOURCE_MEDIA
            # The Resolve 17 scripting API docs mention for ExportTimeline:
            # exportType = 0 for AAF, 1 for DRT, 2 for XML, 3 for EDL etc.
            # It doesn't explicitly list subtypes for AAF in the simple ExportTimeline call signature, 
            # but Project.ExportAAF might have more detailed options.
            # Let's try without subtype first, as it's optional in the signature.
            
            success = timeline.Export(output_filepath, self.resolve.EXPORT_AAF, self.resolve.EXPORT_AAF_NEW)

            if success:
                logger.info(f"Successfully exported timeline '{timeline_name}' to '{output_filepath}'")
                return output_filepath # Return the path on success
            else:
                logger.error(f"Failed to export timeline '{timeline_name}' as AAF. Resolve API returned failure.")
                return False
        except AttributeError as ae:
            logger.error(f"Error accessing DaVinciResolveScript constants (e.g., EXPORT_AAF): {ae}")
            logger.error("This might indicate an issue with the DaVinci Resolve scripting environment or an incorrect constant name.")
            return False
        except Exception as e:
            logger.error(f"Error exporting timeline as AAF: {e}", exc_info=True)
            return False 