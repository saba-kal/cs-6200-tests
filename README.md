# cs-6200-tests
Automated testing suite for a simple distributed file system. The system was built for Graduate Intro to Operating Systems (CS-6200): a Georgia Tech Master's in Online Computer Science course. The actual distributed file system is not included in this repository to avoid code sharing violations.

There are two python scripts:
- tests-grpc-py: These test the various gRPC methods used by the distributed file system. Some of the tests verify functionality by checking the client programs console output, so it may not work for your project.
- tests-dfs.py: This is an unfinished testing suite that was meant to test synchronization between client and server. However, it currently only verifies that the client does not download duplicate files.
