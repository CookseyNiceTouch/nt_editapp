import logging
import sys
import os

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