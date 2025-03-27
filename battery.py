import os
import re
import subprocess
import tempfile
# This is entirely written using AI.
# This script checks the battery health of a Windows laptop by generating a battery report using the powercfg command.
# It extracts the design capacity and full charge capacity from the report and calculates the battery health as a percentage.
def get_battery_health():
    """
    Calculate battery health by comparing full charge capacity to design capacity.
    Returns battery health as a percentage.
    """
    # Create a temporary file for the battery report
    temp_dir = tempfile.gettempdir()
    battery_report_path = os.path.join(temp_dir, "battery_report.html")
    
    try:
        # Generate battery report using Windows powercfg command
        subprocess.run(["powercfg", "/batteryreport", "/output", battery_report_path], 
                      check=True, capture_output=True)
        
        # Read the battery report
        with open(battery_report_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Extract design capacity using regex - include decimal points
        design_capacity_match = re.search(r'<span class="label">DESIGN CAPACITY</span>.*?(\d+(?:\.\d+)?)', 
                                         html_content, re.DOTALL)
        if not design_capacity_match:
            return "Could not find design capacity in battery report"
        
        design_capacity_str = design_capacity_match.group(1)
        
        # Extract full charge capacity using regex - include decimal points
        full_capacity_match = re.search(r'<span class="label">FULL CHARGE CAPACITY</span>.*?(\d+(?:\.\d+)?)', 
                                       html_content, re.DOTALL)
        if not full_capacity_match:
            return "Could not find full charge capacity in battery report"
        
        full_capacity_str = full_capacity_match.group(1)
        # Check if design capacity has decimal point (meaning it's in Wh instead of mWh)
        if '.' in design_capacity_str:
            # Convert Wh to mWh (multiply by 1000)
            design_capacity = float(design_capacity_str) * 1000
        else:
            design_capacity = float(design_capacity_str)
            
        # Do the same for full capacity
        if '.' in full_capacity_str:
            full_capacity = float(full_capacity_str) * 1000
        else:
            full_capacity = float(full_capacity_str)
        
        # Calculate battery health
        battery_health = min(round((full_capacity / design_capacity) * 100, 1), 100)
        
        return battery_health
    except subprocess.CalledProcessError as e:
        return f"Error running powercfg: {e}"
    except FileNotFoundError:
        return "Battery report file not found"
    except Exception as e:
        return f"Error: {e}"
    finally:
        # Clean up - remove temporary file
        if os.path.exists(battery_report_path):
            try:
                os.remove(battery_report_path)
            except:
                pass

def main():
    print("Checking battery health...")
    result = get_battery_health()
    
    if isinstance(result, dict):
        for key, value in result.items():
            print(f"{key}: {value}")
    else:
        print(result)

if __name__ == "__main__":
    main()
