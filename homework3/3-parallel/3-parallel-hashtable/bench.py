import traceback
import sys, os, subprocess, signal
import subprocess as sp

testConfig = [
    {
        "name" : "T1",
        "entries" : 10 ** 6,
        "chunks" : 2,
        "speed" : 0,
        "points" : 15
    },
    {
        "name" : "T2",
        "entries" : 2 * 10 ** 6,
        "chunks" : 2,
        "speed" : 20,
        "points" : 15
    },
    {
        "name" : "T3",
        "entries" : 4 * 10 ** 6,
        "chunks" : 4,
        "speed" : 40,
        "points" : 15
    },
    {
        "name" : "T4",
        "entries" : 8 * 10 ** 7,
        "chunks" : 4,
        "speed" : 50,
        "points" : 15
     },
     {
        "name" : "T5",
        "entries" : 10 ** 8,
        "chunks" : 2,
        "speed" : 50,
        "points" : 10
     },
     {
        "name" : "T6",
        "entries" : 10 ** 8,
        "chunks" : 10,
        "speed" : 50,
        "points" : 10
     },
]

outfile = open('output', 'w')

if len(sys.argv) > 1:
    benchtypes = sys.argv[1:]
else:
    benchtypes = ('0', '1')

hwMaxPoints = 0
hwPoints = 0

for testEntry in testConfig:

    testName = testEntry["name"]
    testEntries = str(testEntry["entries"])
    testChunks = str(testEntry["chunks"])
    testSpeed = str(testEntry["speed"])
    testPoints = testEntry["points"]
    hwMaxPoints += testPoints

    print "\n\n\n------- Test", testName, "START\t----------\n" 

    try:
        child = sp.Popen( ['./gpu_hashtable', testEntries, testChunks, testSpeed], stdout=sp.PIPE )
        output = child.communicate()[0]
        lines = str(output).split("\n")
        print( output )
        rc = child.poll()
        if rc == 1:
            print "------- Test", testName, "END\t---------- \t [ FAILED ]"
            continue

    except Exception:

        print "------- Test", testName, "END\t---------- \t [ FAILED ]"
        traceback.print_exc()
        print "Error with",  str(['./src/gpu_hashtable', testEntries, testChunks, testSpeed])
        continue

    print "------- Test ", testName, "END\t---------- \t [ OK RESULT: ", testPoints, " pts ]"
    hwPoints = hwPoints + testPoints

    print "\nTotal so far: ", hwPoints, "/",  80

print "\nTotal:", hwPoints, "/",  80

