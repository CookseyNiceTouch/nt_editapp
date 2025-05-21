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