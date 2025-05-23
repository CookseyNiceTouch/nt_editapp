# This file will contain the logic for loading and parsing AAF files.
# We aim to convert AAF content into a JSON format compatible with the
# editgenerator module's output, using the pyaaf2 library.

import aaf2 # For reading AAF files
import aaf2.components # For type checking Sequence objects
import os
import json # For the example usage
import urllib.parse # Add this at the top of the file if not already present

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

        extracted_source_filename = input_aaf_filename # Default to AAF filename
        source_filename_found = False

        fps = 30.0 
        if hasattr(main_composition, 'slots'):
            for slot in main_composition.slots:
                if hasattr(slot.segment, 'media_kind') and slot.segment.media_kind.lower() == 'picture':
                    if hasattr(slot, 'edit_rate') and slot.edit_rate:
                         fps = float(slot.edit_rate) 
                         break
                elif hasattr(slot.segment, 'component_data_definition'):
                    pass # Placeholder for more complex DataDef lookup if needed

        json_output = {
            "file_name": extracted_source_filename, # Will be updated if a better name is found
            "fps": fps,
            "target_duration_frames": 0, 
            "actual_duration_frames": 0,
            "segments": []
        }

        segment_id_counter = 1
        cumulative_duration_frames = 0

        if hasattr(main_composition, 'slots'):
            print(f"\n--- Debug: Iterating slots for composition: {main_composition.name if hasattr(main_composition, 'name') else 'N/A'} ---")
            for slot_index, slot in enumerate(main_composition.slots):
                original_segment = slot.segment 
                print(f"\n  Slot {slot_index + 1}: {slot.name if slot.name else 'Unnamed Slot'} (ID: {slot.slot_id if hasattr(slot, 'slot_id') else 'N/A'})")
                print(f"    Segment Type: {type(original_segment)}")
                
                if hasattr(original_segment, 'name') and original_segment.name:
                    print(f"    Segment Name: {original_segment.name}")
                if hasattr(original_segment, 'start'): 
                    print(f"    Segment Start on Main Timeline: {original_segment.start}")
                if hasattr(original_segment, 'length'):
                    print(f"    Segment Length on Main Timeline: {original_segment.length}")
                if hasattr(original_segment, 'media_kind'):
                    print(f"    Segment Media Kind: {original_segment.media_kind}")

                if isinstance(original_segment, aaf2.components.Sequence):
                    print(f"    -> This slot is a Sequence. Iterating its components...")
                    current_offset_in_sequence = 0 

                    for component_index, component in enumerate(original_segment.components):
                        print(f"      Component {component_index + 1} in Sequence: Type = {type(component)}")
                        if hasattr(component, 'name') and component.name:
                            print(f"        Component Name: {component.name}")
                        
                        actual_component_start = None
                        actual_component_length = None
                        if hasattr(component, 'start'):
                             actual_component_start = component.start
                             print(f"        Component Start: {actual_component_start}")
                        if hasattr(component, 'length'):
                             actual_component_length = component.length
                             print(f"        Component Length: {actual_component_length}")

                        if isinstance(component, aaf2.components.SourceClip):
                            if not source_filename_found: 
                                source_mob = None 
                                try:
                                    if hasattr(component, 'mob_id') and component.mob_id:
                                        mob_id_to_lookup = component.mob_id
                                        if mob_id_to_lookup in aaf_file_object.content.mobs:
                                            source_mob = aaf_file_object.content.mobs[mob_id_to_lookup]
                                            print(f"        Found SourceMob via component.mob_id lookup (Mob Name: {source_mob.name if hasattr(source_mob, 'name') else 'N/A'}, ID: {source_mob.mob_id if source_mob else 'N/A'})")
                                            # if source_mob: # dir() print was here, commented out
                                            #     print(f"          DEBUG dir(source_mob): {dir(source_mob)}")
                                        else:
                                            print(f"        Warning: component.mob_id {mob_id_to_lookup} not found in aaf_file_object.content.mobs")
                                    else:
                                        print(f"        Warning: SourceClip component has no 'mob_id' attribute to look up its SourceMob.")

                                    if source_mob:
                                        print(f"        Processing SourceMob for filename: {source_mob.name if hasattr(source_mob, 'name') else 'N/A'} (ID: {source_mob.mob_id})")
                                        
                                        # --- BEGIN DETAILED DEBUG FOR FIRST SOURCEMOB ---
                                        # (The extensive debug block will be removed)
                                        # --- END DETAILED DEBUG FOR FIRST SOURCEMOB ---

                                        filename_from_mob_name = None
                                        if hasattr(source_mob, 'name') and source_mob.name:
                                            filename_from_mob_name = source_mob.name
                                            print(f"          --> Candidate filename from SourceMob.name: {filename_from_mob_name}")

                                        # This is where we try to find the descriptor that has locators
                                        # It might be on the current source_mob, or on a mob referenced by a SourceClip within this source_mob's slots
                                        descriptor_mob = source_mob # Start by assuming the current source_mob has the descriptor
                                        descriptor_found_on_derived_mob = False

                                        # Check if slots in the current source_mob point to another mob that might have the descriptor
                                        if hasattr(source_mob, 'slots'):
                                            temp_slots_iterable = None
                                            if source_mob.slots and hasattr(source_mob.slots, '__iter__'):
                                                temp_slots_iterable = list(source_mob.slots)
                                            if temp_slots_iterable:
                                                for temp_slot in temp_slots_iterable:
                                                    if hasattr(temp_slot, 'segment') and isinstance(temp_slot.segment, aaf2.components.SourceClip):
                                                        inner_source_clip = temp_slot.segment
                                                        if inner_source_clip.get('SourceID') and inner_source_clip.get('SourceID').value:
                                                            physical_mob_id = inner_source_clip.get('SourceID').value
                                                            if physical_mob_id in aaf_file_object.content.mobs:
                                                                potential_descriptor_mob = aaf_file_object.content.mobs[physical_mob_id]
                                                                print(f"            Found a SourceClip in '{source_mob.name}' slot pointing to another Mob (Name: {potential_descriptor_mob.name if hasattr(potential_descriptor_mob, 'name') else 'N/A'}, ID: {physical_mob_id}). Will check this for descriptor.")
                                                                descriptor_mob = potential_descriptor_mob # This is now our primary candidate for descriptor
                                                                descriptor_found_on_derived_mob = True
                                                                break # Found a potential candidate, use this one
                                                    if descriptor_found_on_derived_mob: break

                                        # Now, try to get descriptor from 'descriptor_mob' (either original source_mob or the one derived from its slot's SourceClip)
                                        filename_from_locator = None
                                        descriptor = None

                                        # Attempt 0: Directly check descriptor_mob.descriptor
                                        if hasattr(descriptor_mob, 'descriptor') and descriptor_mob.descriptor and isinstance(descriptor_mob.descriptor, aaf2.core.AAFObject):
                                            descriptor = descriptor_mob.descriptor
                                            print(f"            Found Descriptor via .descriptor on Mob '{descriptor_mob.name if hasattr(descriptor_mob, 'name') else descriptor_mob.mob_id}': Type={type(descriptor)}")

                                        # Attempt 1: descriptor_mob.get("EssenceDescription")
                                        if not descriptor and hasattr(descriptor_mob, 'get'):
                                            try:
                                                potential_desc = descriptor_mob.get("EssenceDescription")
                                                if potential_desc and isinstance(potential_desc, aaf2.core.AAFObject):
                                                    descriptor = potential_desc
                                                    print(f"            Found Descriptor via .get('EssenceDescription') on Mob '{descriptor_mob.name if hasattr(descriptor_mob, 'name') else descriptor_mob.mob_id}': Type={type(descriptor)}")
                                            except Exception as e_get_desc:
                                                print(f"            Tried .get('EssenceDescription') on Mob '{descriptor_mob.name if hasattr(descriptor_mob, 'name') else descriptor_mob.mob_id}' but failed: {e_get_desc}")
                                        
                                        # Attempt 2: Iterate descriptor_mob.slots (if it has slots and descriptor still not found)
                                        if not descriptor and hasattr(descriptor_mob, 'slots'):
                                            dm_slots_iterable = None
                                            if descriptor_mob.slots and hasattr(descriptor_mob.slots, '__iter__'):
                                                dm_slots_iterable = list(descriptor_mob.slots) 
                                            
                                            if dm_slots_iterable:
                                                print(f"            Descriptor not found directly on Mob '{descriptor_mob.name if hasattr(descriptor_mob, 'name') else descriptor_mob.mob_id}', checking its {len(dm_slots_iterable)} slots...")
                                                for i, dm_slot in enumerate(dm_slots_iterable):
                                                    print(f"              Checking Slot {i+1} of Mob '{descriptor_mob.name if hasattr(descriptor_mob, 'name') else descriptor_mob.mob_id}': Name={dm_slot.name if hasattr(dm_slot, 'name') else 'N/A'}, Segment Type={type(dm_slot.segment)}")
                                                    
                                                    # Check dm_slot (the MobSlot itself) for descriptor
                                                    if hasattr(dm_slot, 'descriptor') and dm_slot.descriptor and isinstance(dm_slot.descriptor, aaf2.core.AAFObject):
                                                        descriptor = dm_slot.descriptor
                                                        print(f"                Found Descriptor directly on Slot: Type={type(descriptor)}")
                                                        break 
                                                    elif hasattr(dm_slot, 'get'):
                                                        try:
                                                            potential_desc_on_slot = dm_slot.get("EssenceDescription")
                                                            if potential_desc_on_slot and isinstance(potential_desc_on_slot, aaf2.core.AAFObject):
                                                                descriptor = potential_desc_on_slot
                                                                print(f"                Found Descriptor via Slot.get('EssenceDescription'): Type={type(descriptor)}")
                                                                break
                                                        except Exception as e_get_desc_slot_itself:
                                                            print(f"                Tried Slot.get('EssenceDescription') but failed: {e_get_desc_slot_itself}")
                                                    
                                                    if not descriptor and hasattr(dm_slot, 'segment'):
                                                        current_dm_slot_segment = dm_slot.segment
                                                        if hasattr(current_dm_slot_segment, 'descriptor') and current_dm_slot_segment.descriptor and isinstance(current_dm_slot_segment.descriptor, aaf2.core.AAFObject): 
                                                            descriptor = current_dm_slot_segment.descriptor
                                                            print(f"                Found Descriptor in slot segment's .descriptor: Type={type(descriptor)}")
                                                            break
                                                        elif hasattr(current_dm_slot_segment, 'get'): 
                                                            try:
                                                                potential_desc_in_segment = current_dm_slot_segment.get("EssenceDescription")
                                                                if potential_desc_in_segment and isinstance(potential_desc_in_segment, aaf2.core.AAFObject):
                                                                    descriptor = potential_desc_in_segment
                                                                    print(f"                Found Descriptor via slot.segment.get('EssenceDescription'): Type={type(descriptor)}")
                                                                    break
                                                            except Exception as e_get_desc_slot_segment:
                                                                print(f"                Tried slot.segment.get('EssenceDescription') but failed: {e_get_desc_slot_segment}")
                                                    if descriptor: break # Found descriptor in this slot or its segment
                                            else:
                                                print(f"            Mob '{descriptor_mob.name if hasattr(descriptor_mob, 'name') else descriptor_mob.mob_id}' has no .slots or .slots is not iterable/empty.")

                                        if descriptor:
                                            print(f"            Using Descriptor: Type={type(descriptor)}")
                                            # --- DETAILED DEBUG FOR THE FOUND DESCRIPTOR (now removed) ---
                                            # print(f"              DEBUG dir(descriptor): {dir(descriptor)}")
                                            # ... (rest of descriptor debug prints removed) ...
                                            # --- END DETAILED DEBUG ---

                                            locators_to_check = None
                                            # The descriptor itself (e.g., CDCIDescriptor) should have a "Locator" property
                                            # which is a StrongRefVectorProperty. Its .value will be a list of actual Locator objects.
                                            locator_property = descriptor.get('Locator') # Use .get() for safety
                                            if locator_property and hasattr(locator_property, 'value') and locator_property.value:
                                                candidate_list = locator_property.value
                                                if hasattr(candidate_list, '__iter__') and not isinstance(candidate_list, (str, bytes)):
                                                    locators_to_check = list(candidate_list)
                                                    if locators_to_check:
                                                        print(f"              Found locators via descriptor.get('Locator').value: Count={len(locators_to_check)}, Types={[type(loc) for loc in locators_to_check]}")
                                                elif isinstance(candidate_list, aaf2.core.AAFObject): # Single locator object
                                                    locators_to_check = [candidate_list]
                                                    if locators_to_check:
                                                        print(f"              Found single locator via descriptor.get('Locator').value: Type={type(candidate_list)}")
                                            
                                            if not locators_to_check:
                                                # Fallback: what if descriptor.locator directly gives the list or single object?
                                                if hasattr(descriptor, 'locator') and descriptor.locator:
                                                    candidate_direct = descriptor.locator
                                                    if hasattr(candidate_direct, 'value') and candidate_direct.value: # If it's a property object
                                                        candidate_direct = candidate_direct.value

                                                    if hasattr(candidate_direct, '__iter__') and not isinstance(candidate_direct, (str, bytes)):
                                                        locators_to_check = list(candidate_direct)
                                                        if locators_to_check:
                                                            print(f"              Found locators via descriptor.locator (after .value if applicable): Count={len(locators_to_check)}")
                                                    elif isinstance(candidate_direct, aaf2.core.AAFObject):
                                                        locators_to_check = [candidate_direct]
                                                        if locators_to_check:
                                                            print(f"              Found single locator via descriptor.locator (after .value if applicable)")

                                            if locators_to_check:
                                                print(f"              Processing {len(locators_to_check)} locator object(s)...")
                                                for locator_index, actual_locator_obj in enumerate(locators_to_check):
                                                    print(f"                Locator {locator_index+1}: Object Type = {type(actual_locator_obj)}")
                                                    # --- DEBUG FOR THE ACTUAL LOCATOR OBJECT ---
                                                    print(f"                  DEBUG dir(actual_locator_obj): {dir(actual_locator_obj)}")
                                                    try:
                                                        print(f"                    DEBUG actual_locator_obj.allkeys(): {list(actual_locator_obj.allkeys())}")
                                                        for key in actual_locator_obj.allkeys():
                                                            try:
                                                                value = actual_locator_obj.get(key)
                                                                val_value = value.value if hasattr(value, 'value') else "N/A (no .value attr or value is None)"
                                                                if isinstance(val_value, bytes): # Decode if bytes (like URLString data)
                                                                    try:
                                                                        val_value = val_value.decode('utf-16le', 'strict')
                                                                    except UnicodeDecodeError:
                                                                        try:
                                                                            val_value = val_value.decode('utf-8', 'strict')
                                                                        except UnicodeDecodeError:
                                                                            val_value = f"BYTES (undecodable): {val_value[:50]}..."

                                                                print(f"                      LocObj_Key '{key}': {value} (Type: {type(value)}), Value: {val_value}")
                                                                
                                                                # Specifically look for 'Path' or 'URLString' to extract filename
                                                                if key in ['Path', 'URLString'] and val_value and isinstance(val_value, str):
                                                                    filename_from_locator = os.path.basename(val_value)
                                                                    # Basic file URI handling
                                                                    if filename_from_locator.lower().startswith('file://'):
                                                                        parsed_url = urllib.parse.urlparse(val_value)
                                                                        filename_from_locator = os.path.basename(urllib.parse.unquote(parsed_url.path))

                                                                    print(f"                        --> Extracted filename from locator key '{key}': {filename_from_locator}")
                                                                    # source_filename_found = True # This will be set outside loop if filename_from_locator is set
                                                                    break # Found a path from this locator, stop checking its keys
                                                            except Exception as e_loc_key:
                                                                print(f"                      LocObj_Key '{key}': Error getting/printing value: {e_loc_key}")
                                                        if filename_from_locator: break # Found filename, break from locators loop
                                                    except Exception as e_loc_detail_debug:
                                                        print(f"                    Error during locator detailed debug print: {e_loc_detail_debug}")
                                                    # --- END DEBUG FOR ACTUAL LOCATOR ---
                                                    if filename_from_locator: break # Found filename, break from locators loop (redundant, but safe)
                                            else:
                                                print(f"              Descriptor '{descriptor.name if hasattr(descriptor, 'name') else type(descriptor)}' has no 'Locator' property with a valid list/object, or it was empty.")
                                        else:
                                            print(f"            Could not find a valid EssenceDescriptor for this SourceMob ({source_mob.name}).")
                                        
                                        if filename_from_locator:
                                            extracted_source_filename = filename_from_locator
                                            source_filename_found = True
                                        elif filename_from_mob_name: 
                                            extracted_source_filename = filename_from_mob_name
                                            source_filename_found = True
                                            print(f"          --> Using SourceMob.name ('{filename_from_mob_name}') as fallback filename since no locator path found/suitable.")
                                        else:
                                            print(f"          --> Neither SourceMob.name nor locator path yielded a usable filename for {source_mob.name}.")
                                        
                                        if source_filename_found: 
                                            # This break is for the "if not source_filename_found:" block's purpose - to stop trying to find the filename.
                                            # It does NOT break from iterating components for the segments list.
                                            pass # Filename is found, no need to break, the flag handles it.

                                except Exception as e_mob_lookup:
                                    print(f"        Warning: Error during SourceMob/filename lookup for a clip: {e_mob_lookup}") 
                            
                            # This part adds the current component (clip) to the segments list
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
                                print(f"        --> Added SourceClip (type check) to JSON: {segment_data}")
                            else:
                                print(f"        --> Skipped SourceClip due to missing start/length.")
                        
                        if actual_component_length is not None:
                            current_offset_in_sequence += int(actual_component_length)
                
                elif isinstance(original_segment, aaf2.components.SourceClip):
                    if hasattr(original_segment, 'start') and original_segment.start is not None and \
                       hasattr(original_segment, 'length') and original_segment.length is not None:
                        
                        if not source_filename_found: # Try to get filename for top-level source clips too
                            # Simplified filename logic for top-level clips, can be expanded if necessary
                            if hasattr(original_segment, 'mob_id') and original_segment.mob_id:
                                top_level_sc_mob = aaf_file_object.content.mobs.get(original_segment.mob_id)
                                if top_level_sc_mob and hasattr(top_level_sc_mob, 'name') and top_level_sc_mob.name:
                                    extracted_source_filename = top_level_sc_mob.name
                                    source_filename_found = True
                                    print(f"    --> Using SourceMob.name for top-level SourceClip: {extracted_source_filename}")
                        
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
                        print(f"    --> Added top-level SourceClip to JSON: {segment_data}")

        print(f"--- Debug: Final extracted_source_filename before assigning to json_output: {extracted_source_filename} (Found: {source_filename_found}) ---")
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
            # Using json.dumps for pretty printing
            print(json.dumps(json_output, indent=2))
        else:
            print("\nFailed to process AAF file. Check errors above.") 