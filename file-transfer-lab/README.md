
* lab is in the file-transfer-lab subdir
* work with and without the proxy
* support multiple clients simultaneously using `fork()`
* gracefully deal with scenarios such as:
    * zero length files
    * user attempts to transmit a file which does not exist
    * file already exists on the server
    * the client or server unexpectedly disconnect
