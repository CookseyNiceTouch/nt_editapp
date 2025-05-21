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
            import DaVinciResolveScript as dvr_script
        except ImportError as e:
            logger.error('Could not import DaVinciResolveScript: %s', e)
            raise
        
        # Try to get resolve object
        try:
            self.resolve = dvr_script.scriptapp('Resolve')
            if not self.resolve:
                raise RuntimeError('Could not connect to DaVinci Resolve instance.')
            logger.debug('Connected to DaVinci Resolve instance.')
        except Exception as e:
            logger.error('Failed to connect to DaVinci Resolve: %s', e)
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