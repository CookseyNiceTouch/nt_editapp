# This file will contain the logic for loading and parsing AAF files.
# We aim to convert AAF content into a JSON format compatible with the
# editgenerator module's output, using the pyaaf2 library.
#
# AAF (Advanced Authoring Format) files are complex, structured containers used in professional video and audio post-production.
# At a high level, an AAF file typically contains:
# 1.  Header: Metadata about the AAF file itself (e.g., creation tool, version).
# 2.  Dictionary: Definitions of classes and types used within the AAF file.
# 3.  Content Storage: This is the core, containing various "Mobs" (Media OBjects).
#     - CompositionMobs: Represent sequences or timelines. They have "Slots" (tracks) which contain segments like SourceClips, Transitions, Fillers, or NestedSequences.
#     - SourceClips on a timeline point to SourceMobs (or MasterMobs/FileMobs) via a MobID.
#     - SourceMobs (often MasterMobs or FileSourceMobs) represent the actual source media (e.g., a video or audio file).
#       These mobs usually contain an EssenceDescriptor (e.g., CDCIDescriptor for video, WaveAudioDescriptor for audio)
#       which describes the media's technical characteristics (codec, sample rate, frame size, etc.).
#     - The EssenceDescriptor, in turn, typically holds one or more Locator objects (e.g., NetworkLocator)
#       that provide the file path or URI to the external media file.
# The challenge in parsing AAFs often lies in navigating these relationships, as information like file paths can be several indirections away from the timeline clip.

import aaf2 # For reading AAF files
import aaf2.components # For type checking Sequence objects
import os
import json # For the example usage
import urllib.parse # For parsing file URIs from locators

# The load_aaf_file function is no longer needed with pyaaf2's context manager.

def parse_aaf_to_json(aaf_file_object, input_aaf_filename="unknown.aaf"):
    """
    Parses the AAF data using a pyaaf2 file object and converts it into the target JSON structure.

    Args:
        aaf_file_object: The pyaaf2 file object obtained from aaf2.open().
        input_aaf_filename (str): The original name of the AAF file being processed.

    Returns:
        dict: A dictionary representing the JSON output.
              Returns None if parsing fails.
    """
    try:
        main_composition = next(aaf_file_object.content.toplevel())
        if not main_composition:
            print(f"Error: Could not find a main composition in {input_aaf_filename}")
            return None

        extracted_source_filename = input_aaf_filename 
        source_filename_found = False

        fps = 30.0 
        if hasattr(main_composition, 'slots'):
            for slot in main_composition.slots:
                if hasattr(slot.segment, 'media_kind') and slot.segment.media_kind.lower() == 'picture':
                    if hasattr(slot, 'edit_rate') and slot.edit_rate:
                         fps = float(slot.edit_rate) 
                         break
                elif hasattr(slot.segment, 'component_data_definition'):
                    pass 

        json_output = {
            "file_name": extracted_source_filename, 
            "fps": fps,
            "target_duration_frames": 0, 
            "actual_duration_frames": 0,
            "segments": []
        }

        segment_id_counter = 1
        cumulative_duration_frames = 0

        if hasattr(main_composition, 'slots'):
            for slot_index, slot in enumerate(main_composition.slots):
                original_segment = slot.segment 
                if isinstance(original_segment, aaf2.components.Sequence):
                    current_offset_in_sequence = 0 

                    for component_index, component in enumerate(original_segment.components):
                        actual_component_start = None
                        actual_component_length = None
                        if hasattr(component, 'start'):
                             actual_component_start = component.start
                        if hasattr(component, 'length'):
                             actual_component_length = component.length

                        if isinstance(component, aaf2.components.SourceClip):
                            if not source_filename_found: 
                                source_mob = None 
                                try:
                                    if hasattr(component, 'mob_id') and component.mob_id:
                                        mob_id_to_lookup = component.mob_id
                                        if mob_id_to_lookup in aaf_file_object.content.mobs:
                                            source_mob = aaf_file_object.content.mobs[mob_id_to_lookup]
                                        else:
                                            print(f"        Warning: component.mob_id {mob_id_to_lookup} not found in aaf_file_object.content.mobs")
                                    else:
                                        print(f"        Warning: SourceClip component has no 'mob_id' attribute to look up its SourceMob.")

                                    if source_mob:
                                        # The source_mob obtained from the timeline SourceClip (component.mob_id)
                                        # might not directly contain the EssenceDescriptor with locators.
                                        # Often, it's a "master" or "file" source mob, referenced *by* a SourceClip
                                        # within this initial source_mob's slots, that holds the actual descriptor.

                                        filename_from_mob_name = None
                                        if hasattr(source_mob, 'name') and source_mob.name:
                                            filename_from_mob_name = source_mob.name

                                        # descriptor_mob will be the mob we ultimately try to get an EssenceDescriptor from.
                                        # Start by assuming the current source_mob is the one.
                                        descriptor_mob = source_mob 
                                        descriptor_found_on_derived_mob = False # Flag to indicate if we switched to a mob referenced by an inner SourceClip

                                        # Step 1: Check if any SourceClip within the current source_mob's slots points to a different Mob.
                                        # This different Mob is often the actual FileSourceMob or MasterMob with the descriptor.
                                        if hasattr(source_mob, 'slots'):
                                            temp_slots_iterable = None
                                            if source_mob.slots and hasattr(source_mob.slots, '__iter__'):
                                                temp_slots_iterable = list(source_mob.slots)
                                            if temp_slots_iterable:
                                                for temp_slot in temp_slots_iterable:
                                                    if hasattr(temp_slot, 'segment') and isinstance(temp_slot.segment, aaf2.components.SourceClip):
                                                        inner_source_clip = temp_slot.segment
                                                        # This inner SourceClip's 'SourceID' points to the MobID of the (potentially) actual descriptor-holding Mob.
                                                        if inner_source_clip.get('SourceID') and inner_source_clip.get('SourceID').value:
                                                            physical_mob_id = inner_source_clip.get('SourceID').value
                                                            if physical_mob_id in aaf_file_object.content.mobs:
                                                                potential_descriptor_mob = aaf_file_object.content.mobs[physical_mob_id]
                                                                descriptor_mob = potential_descriptor_mob # Switch to this mob for descriptor search.
                                                                descriptor_found_on_derived_mob = True
                                                                break # Found a candidate mob via indirection, use this one.
                                                    if descriptor_found_on_derived_mob: break # Exit outer loop once a derived mob is found.

                                        # Step 2: Attempt to get the EssenceDescriptor from the determined descriptor_mob.
                                        filename_from_locator = None
                                        descriptor = None

                                        # Attempt 2a: Directly check descriptor_mob.descriptor attribute.
                                        if hasattr(descriptor_mob, 'descriptor') and descriptor_mob.descriptor and isinstance(descriptor_mob.descriptor, aaf2.core.AAFObject):
                                            descriptor = descriptor_mob.descriptor

                                        # Attempt 2b: Try descriptor_mob.get("EssenceDescription") method/property.
                                        if not descriptor and hasattr(descriptor_mob, 'get'):
                                            try:
                                                potential_desc = descriptor_mob.get("EssenceDescription")
                                                if potential_desc and isinstance(potential_desc, aaf2.core.AAFObject):
                                                    descriptor = potential_desc
                                            except Exception as e_get_desc:
                                                print(f"            Warning: Tried .get('EssenceDescription') on Mob '{descriptor_mob.name if hasattr(descriptor_mob, 'name') else descriptor_mob.mob_id}' but failed: {e_get_desc}")
                                        
                                        # Attempt 2c: If still no descriptor, iterate descriptor_mob's slots.
                                        # The descriptor might be on a slot itself or its segment.
                                        if not descriptor and hasattr(descriptor_mob, 'slots'):
                                            dm_slots_iterable = None
                                            if descriptor_mob.slots and hasattr(descriptor_mob.slots, '__iter__'):
                                                dm_slots_iterable = list(descriptor_mob.slots) 
                                            
                                            if dm_slots_iterable:
                                                for i, dm_slot in enumerate(dm_slots_iterable):
                                                    # Check the MobSlot itself for a descriptor.
                                                    if hasattr(dm_slot, 'descriptor') and dm_slot.descriptor and isinstance(dm_slot.descriptor, aaf2.core.AAFObject):
                                                        descriptor = dm_slot.descriptor
                                                        break 
                                                    elif hasattr(dm_slot, 'get'):
                                                        try:
                                                            potential_desc_on_slot = dm_slot.get("EssenceDescription")
                                                            if potential_desc_on_slot and isinstance(potential_desc_on_slot, aaf2.core.AAFObject):
                                                                descriptor = potential_desc_on_slot
                                                                break
                                                        except Exception as e_get_desc_slot_itself:
                                                            print(f"                Warning: Tried Slot.get('EssenceDescription') but failed: {e_get_desc_slot_itself}")
                                                    
                                                    # If not on slot, check its segment.
                                                    if not descriptor and hasattr(dm_slot, 'segment'):
                                                        current_dm_slot_segment = dm_slot.segment
                                                        if hasattr(current_dm_slot_segment, 'descriptor') and current_dm_slot_segment.descriptor and isinstance(current_dm_slot_segment.descriptor, aaf2.core.AAFObject): 
                                                            descriptor = current_dm_slot_segment.descriptor
                                                            break
                                                        elif hasattr(current_dm_slot_segment, 'get'): 
                                                            try:
                                                                potential_desc_in_segment = current_dm_slot_segment.get("EssenceDescription")
                                                                if potential_desc_in_segment and isinstance(potential_desc_in_segment, aaf2.core.AAFObject):
                                                                    descriptor = potential_desc_in_segment
                                                                    break
                                                            except Exception as e_get_desc_slot_segment:
                                                                print(f"                Warning: Tried slot.segment.get('EssenceDescription') but failed: {e_get_desc_slot_segment}")
                                                    if descriptor: break # Found descriptor, exit slot iteration.

                                        # Step 3: If an EssenceDescriptor was found, try to get Locators from it.
                                        if descriptor:
                                            locators_to_check = None
                                            # EssenceDescriptors (like CDCIDescriptor) should have a 'Locator' property.
                                            # This property (a StrongRefVectorProperty) typically holds a list of actual Locator objects in its .value.
                                            locator_property = descriptor.get('Locator') 
                                            if locator_property and hasattr(locator_property, 'value') and locator_property.value:
                                                candidate_list = locator_property.value
                                                if hasattr(candidate_list, '__iter__') and not isinstance(candidate_list, (str, bytes)):
                                                    locators_to_check = list(candidate_list)
                                                elif isinstance(candidate_list, aaf2.core.AAFObject): # Single locator object
                                                    locators_to_check = [candidate_list]
                                            
                                            # Fallback: try accessing descriptor.locator directly if .get('Locator') failed.
                                            if not locators_to_check:
                                                if hasattr(descriptor, 'locator') and descriptor.locator: # Note: AAF Spec often refers to 'Locator' (plural) but pyaaf2 might expose singular
                                                    candidate_direct = descriptor.locator
                                                    if hasattr(candidate_direct, 'value') and candidate_direct.value: # If it's a property object itself
                                                        candidate_direct = candidate_direct.value # Get its actual value (the list or single locator)

                                                    if hasattr(candidate_direct, '__iter__') and not isinstance(candidate_direct, (str, bytes)):
                                                        locators_to_check = list(candidate_direct)
                                                    elif isinstance(candidate_direct, aaf2.core.AAFObject):
                                                        locators_to_check = [candidate_direct]

                                            # Step 4: If locators are found, iterate them and extract path information.
                                            if locators_to_check:
                                                for locator_index, actual_locator_obj in enumerate(locators_to_check):
                                                    # The actual_locator_obj is usually a NetworkLocator or similar.
                                                    try:
                                                        for key in actual_locator_obj.allkeys(): # Check all properties of the locator object.
                                                            try:
                                                                value_prop = actual_locator_obj.get(key)
                                                                actual_val = value_prop.value if hasattr(value_prop, 'value') else None
                                                                if isinstance(actual_val, bytes): # URLString data can be bytes.
                                                                    try:
                                                                        actual_val = actual_val.decode('utf-16le', 'strict')
                                                                    except UnicodeDecodeError:
                                                                        try:
                                                                            actual_val = actual_val.decode('utf-8', 'strict')
                                                                        except UnicodeDecodeError:
                                                                            actual_val = f"BYTES (undecodable): {actual_val[:50]}..."

                                                                # The NetworkLocator object should have a 'Path' or 'URLString' property containing the file path.
                                                                if key in ['Path', 'URLString'] and actual_val and isinstance(actual_val, str):
                                                                    parsed_url = urllib.parse.urlparse(actual_val)
                                                                    if parsed_url.scheme == 'file':
                                                                        clean_path = parsed_url.path
                                                                        if os.name == 'nt' and clean_path.startswith('/') and clean_path[2] == ':':
                                                                            clean_path = clean_path[1:] # Strip leading / for paths like /C:/...
                                                                        filename_from_locator = os.path.basename(urllib.parse.unquote(clean_path))
                                                                    else:
                                                                        # If not a file URI, assume it's a direct path.
                                                                        filename_from_locator = os.path.basename(actual_val)
                                                                    break # Found a path, exit keys loop for this locator.
                                                            except Exception as e_loc_key:
                                                                print(f"                      Warning: LocObj_Key '{key}': Error getting/printing value: {e_loc_key}")
                                                        if filename_from_locator: break # Filename found, exit locators loop.
                                                    except Exception as e_loc_detail_debug:
                                                        print(f"                    Warning: Error during locator processing: {e_loc_detail_debug}")
                                                    if filename_from_locator: break # Filename found, exit locators loop again (safety).
                                        
                                        # Step 5: Set the extracted filename, falling back to Mob name if necessary.
                                        if filename_from_locator:
                                            extracted_source_filename = filename_from_locator
                                            source_filename_found = True
                                        elif filename_from_mob_name: 
                                            extracted_source_filename = filename_from_mob_name
                                            source_filename_found = True
                                        
                                        if source_filename_found: 
                                            pass 

                                except Exception as e_mob_lookup:
                                    print(f"        Warning: Error during SourceMob/filename lookup for a clip: {e_mob_lookup}") 
                            
                            if actual_component_start is not None and actual_component_length is not None:
                                frame_in = int(actual_component_start)
                                duration_frames = int(actual_component_length)
                                frame_out = frame_in + duration_frames
                                speaker = "" 
                                text = ""    
                                segment_data = {
                                    "segment_id": segment_id_counter,
                                    "speaker": speaker,
                                    "frame_in": frame_in,
                                    "frame_out": frame_out,
                                    "text": text,
                                    "clip_order": segment_id_counter
                                }
                                json_output["segments"].append(segment_data)
                                cumulative_duration_frames += duration_frames
                                segment_id_counter += 1
                        
                        if actual_component_length is not None:
                            current_offset_in_sequence += int(actual_component_length)
                
                elif isinstance(original_segment, aaf2.components.SourceClip):
                    if hasattr(original_segment, 'start') and original_segment.start is not None and \
                       hasattr(original_segment, 'length') and original_segment.length is not None:
                        
                        if not source_filename_found: 
                            if hasattr(original_segment, 'mob_id') and original_segment.mob_id:
                                top_level_sc_mob = aaf_file_object.content.mobs.get(original_segment.mob_id)
                                if top_level_sc_mob and hasattr(top_level_sc_mob, 'name') and top_level_sc_mob.name:
                                    extracted_source_filename = top_level_sc_mob.name
                                    source_filename_found = True
                        
                        frame_in = int(original_segment.start)
                        duration_frames = int(original_segment.length)
                        frame_out = frame_in + duration_frames
                        speaker = "" 
                        text = ""
                        segment_data = {
                            "segment_id": segment_id_counter,
                            "speaker": speaker,
                            "frame_in": frame_in,
                            "frame_out": frame_out,
                            "text": text,
                            "clip_order": segment_id_counter
                        }
                        json_output["segments"].append(segment_data)
                        cumulative_duration_frames += duration_frames
                        segment_id_counter += 1

        json_output["file_name"] = extracted_source_filename
        json_output["actual_duration_frames"] = cumulative_duration_frames
        json_output["target_duration_frames"] = cumulative_duration_frames 
        return json_output

    except Exception as e:
        print(f"Error parsing AAF data from {input_aaf_filename} using pyaaf2: {e}")
        import traceback
        traceback.print_exc()
        return None

def process_aaf_file(file_path):
    """
    Processes an AAF file using pyaaf2, extracts information, and converts it to JSON.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None

    try:
        with aaf2.open(file_path, "r") as f: 
            input_filename = os.path.basename(file_path)
            json_data = parse_aaf_to_json(f, input_aaf_filename=input_filename)
            return json_data
    except Exception as e:
        print(f"Error opening or processing AAF file {file_path} with pyaaf2: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    # --- Simple Tester for AAF Processing ---

    # Default AAF file path. 
    # Workspace root: C:\Users\simon\Development\nt_editapp
    # Relative path from user: NT_EDITAPP\data\exports\Nice_Touch_Timeline.aaf
    # Since the script is within the workspace, we can construct the path relative to the project root or use an absolute one.
    
    # Constructing the path based on the assumption that 'NT_EDITAPP' is the workspace root.
    # For a portable script, it might be better to make this path configurable or relative to the script's location
    # if the 'data' folder is always at a known relative position.
    
    # If your current working directory when running this script is the workspace root (nt_editapp),
    # a relative path like this would work:
    default_aaf_path = os.path.join("data", "exports", "Nice_Touch_Timeline.aaf")
    
    # To use a different file, you can change the line above, for example:
    # default_aaf_path = "path/to/your/other/file.aaf" 
    # Or, you could implement argparse for command-line arguments.

    # You can also provide an absolute path directly if preferred:
    # For example: default_aaf_path = r"C:\Users\simon\Development\nt_editapp\data\exports\Nice_Touch_Timeline.aaf"
    # Ensure the 'r' prefix for raw string if using backslashes on Windows, or use forward slashes.

    print(f"Attempting to process AAF file: {os.path.abspath(default_aaf_path)}")
    if not os.path.exists(default_aaf_path):
        print(f"Error: Default AAF file not found at {os.path.abspath(default_aaf_path)}")
        print("Please ensure the file exists or modify the 'default_aaf_path' in the script.")
    else:
        json_output = process_aaf_file(default_aaf_path)
        if json_output:
            print("\nAAF file processed successfully. JSON output:")
            print(json.dumps(json_output, indent=2))
        else:
            print("\nFailed to process AAF file. Check errors above.") 