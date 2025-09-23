import subprocess

def run_test_script(script_name):
    print(f"\nRunning {script_name}...\n")
    try:
        result = subprocess.run(['python', script_name], capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print("Errors/Warnings:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Test {script_name} failed!")
        print(e.output)
        print(e.stderr)

if __name__ == "__main__":
    test_scripts = [
        "test_env_basic.py",
        "test_curriculum_adjustment.py",
        "test_ppo_training.py",
        "test_render_kernel.py"
        # Add more test scripts here as needed
    ]
    for script in test_scripts:
        run_test_script(script)
