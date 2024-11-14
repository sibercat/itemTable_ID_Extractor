def extract_numbers_from_file(input_file, output_file, keyword):
    """
    Extract row names from a file with automatic encoding detection.
    
    Args:
        input_file: Path to the input file
        output_file: Path to save the extracted row names
        keyword: The keyword to search for in each line
    """
    # Try different encodings
    encodings = ['utf-8', 'utf-16-le', 'utf-16-be', 'ascii', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            output = "("
            with open(input_file, 'r', encoding=encoding) as f_in:
                while True:
                    try:
                        line = f_in.readline()
                        if not line:
                            break
                            
                        if keyword in line:
                            try:
                                splitLine = line.strip().split(": ")
                                if len(splitLine) >= 2:
                                    parsedRowName = splitLine[1][1:-2]
                                    output += f"'{parsedRowName}', "
                            except IndexError:
                                continue  # Skip malformed lines
                    except UnicodeDecodeError:
                        # If we hit a decode error in the middle of the file, 
                        # this encoding is not correct
                        break
                        
            # If we got here without breaking, we successfully read the file
            if output.endswith(", "):
                output = output[:-2]  # Remove last comma and space
            output += ")"
            
            # Write output to file
            with open(output_file, 'w', encoding='utf-8') as f_out:
                f_out.write(output)
                
            print(f"Successfully processed file using {encoding} encoding")
            return
            
        except UnicodeError:
            continue  # Try next encoding
        except Exception as e:
            print(f"Error with {encoding} encoding: {str(e)}")
            continue
            
    raise ValueError(f"Could not process file with any of these encodings: {encodings}")

if __name__ == '__main__':
    try:
        input_file = 'ItemTable.json'
        output_file = 'output.txt'
        keyword = 'RowName'
        
        extract_numbers_from_file(input_file, output_file, keyword)
        print("Done!")
        
    except Exception as e:
        print(f"Error: {str(e)}")