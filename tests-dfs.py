import subprocess
import filecmp
import os.path

# Run the server seperately:
# ./bin/dfs-server-p1 -m ./mnt/server/
# ./bin/dfs-server-p2 -m ./mnt/server/

# Configure test variables here:
client_program = "dfs-client-p2"
client_mount = "/root/projects/pr4/mnt/client/"
server_mount = "/root/projects/pr4/mnt/server/"
print_client_output = True

test_files = ["test-file.html", "big-bear.jpg"]


def main():
    print("\n======= FILE ALREADY EXISTS TEST =======")
    test_file_already_exists()
    print("\n")


def test_file_already_exists():

    file = test_files[0]
    run_client(file, "store")
    if not filecmp.cmp(server_mount + file, client_mount + file, shallow=False):
        print("Store of file " + file + " failed. Result: FAIL")
        return

    # Run client again with the same file.
    output = run_client(file, "store")
    if "already exists" in output.lower():
        print("Store file already exists test: SUCCESS")
    else:
        print("Store file already exists test: FAIL")

    # Run client again to fetch same file.
    output = run_client(file, "fetch")
    if "already exists" in output.lower():
        print("Fetch file already exists test: SUCCESS")
    else:
        print("Fetch file already exists test: FAIL")

    # Delete file to clean up.
    run_client(file, "delete")
    if (os.path.isfile(server_mount + file)):
        print("Delete " + file + ": FAIL")



def run_client(file, command, deadline=9000):
    args = ["./bin/" + client_program, "-m", client_mount, command, file, "-t", str(deadline)]
    result = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = str(result.stdout.read().decode())
    if print_client_output:
        print(output)
    return output


def run_client_list(deadline=9000):
    args = ["./bin/" + client_program, "-m", client_mount, "list", "-t", str(deadline)]
    result = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = str(result.stdout.read().decode())
    print(output)
    return output


if __name__ == "__main__":
    main()