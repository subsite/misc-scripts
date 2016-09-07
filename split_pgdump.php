#!/usr/bin/php -q
<?php

/*
| Yet another schema dump splitter.
| Splits a postgresql schema dump into separate files.
| The bundles rules, indexes, sequences, constraints and such  
| within its parent object file, e.g. the constraints of a table
| is stored in the same file as the table itself.
|
| Include the types you want to create separate files for in
| conf => savetypes. 
|
| USAGE: split_pgdump.php SCHEMA_FILE OUTPUT_DIR
|
| AUTOMATION OPTIONS: 
|   - As a pre-commit hook in a project that uses PostgreSQL
|   - As a cron script
|
| NOTES: 
|   - Tested on PostgreSQL 9.5 only.
|   - Dump using -s (--schema_only) don't know what will happen if run on full dump...
|   - This script will not in any way backup your data
|
*/


$conf = [
    "savetypes" => [ // Database objects stored as separate files
        "TABLE", "VIEW", "FUNCTION", "EXTENSION", "AGGREGATE", "TYPE" 
    ],
    "ignoretypes" => [ // Don't save these types at all
        "ACL", "SEQUENCE", "SEQUENCE OWNED BY", "DEFAULT", "DEFAULT ACL" 
    ]
];

if (empty($argv[1]) || empty($argv[2])) {
    exit("USAGE: split_pgdump.php SCHEMA_FILE OUTPUT_DIR\n");
}

$dumpfile = realpath($argv[1]);
$outdir = realpath($argv[2]);

if (empty($outdir)) {
    exit("ERROR: Bad output OUTPUT_DIR\n");
} else if (empty($dumpfile)) {
    exit("ERROR: SCHEMA_FILE not found\n");
}

echo "Splitting " . $dumpfile . " to " . $outdir . "/";
echo "\n";

// Read dumpfile
$dump = file_get_contents($dumpfile);
// Split dumpfile into array preserving delimiter (header)
$parts = preg_split('/(-- Name: [a-zA-Z0-9 "\(\),:;_-]+)/', $dump, 0, PREG_SPLIT_NO_EMPTY | PREG_SPLIT_DELIM_CAPTURE);

$splitted = [];

foreach($parts as $key => $part) {
    // preg_split will put delimiters in odd keys, so:
    if ($key % 2 == 1) {
        // Get header from part
        $header = substr($parts[$key], 3);
        // Temporarily to JSON 
        $header = '{"' . str_replace(['"', '; ', ': '], ['', '", "', '": "'] ,$header) . '"}';
        // Make assoc array
        $header = (array) json_decode($header);
        
        // Get name, type and query data
        $name = $header["Name"];
        $type = @$header["Type"];
        $data = $parts[$key+1];

        if (in_array($type, $conf["savetypes"]) && !in_array($type, $conf["ignoretypes"])) {
           
            // Name cleanup
            $name = explode(".", $name)[0];
            $name = explode("(", $name)[0];
            $name = str_replace([ 
                "TABLE ", "VIEW ", "COMMENT ON COLUMN ", "COLUMN ", "EXTENSION ", "FUNCTION " 
            ],'',$name);

            // Parse special types to find their parent object name in query
            if ($type == "INDEX") {
                $name = strstr(substr(strstr($data, "ON"), 3), " ", true);
            } else if ($type == "CONSTRAINT" || $type == "FK CONSTRAINT") {
                $name = strstr(substr(strstr($data, "ALTER TABLE ONLY"), 17), "\n", true);
            } else if ($type == "RULE") {
                $name = strstr(substr(strstr($data, "TO"), 3), " ", true);
            }
            $name = str_replace('"','',$name);

            // Create key if needed and parse content
            if (empty($splitted[$name])) {
                $splitted[$name] = ["body" => "", "type" => ""];
                $splitted[$name]["body"] = "-- \n" . $parts[$key];
                $addcontent = $data;
            } else {
                $addcontent = "-- \n" . $parts[$key]. $data;
            }
            
            // Add content to array
            $splitted[$name]["type"] = $type;
            $splitted[$name]["body"] .= substr($addcontent, 0, -3);
            
            
        }
    }
}

// Create files
foreach($splitted as $key => $split) {
    $filename = $outdir . "/" . str_replace(" ", "_", $split["type"] . "_" . $key . ".sql");
    $contents = $split["body"];
    file_put_contents($filename, $contents);
}

exit("Dump splitted into " . count($splitted) . " files.\n");


