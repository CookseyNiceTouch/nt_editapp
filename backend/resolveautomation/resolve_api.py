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
            else:
                logger.warning('Project creation failed: %s', project_name)
            return project
        except Exception as e:
            logger.error('Error creating project: %s', e)
            return None 