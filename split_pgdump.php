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
|   - Dump using -s --schema_only (don't know what will happen if run on full dump)
|   - This script will not in any way backup your data
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

$contents = file_get_contents($dumpfile);
$parts = preg_split('/(-- Name: [a-zA-Z0-9 "\(\),:;_-]+)/', $contents, 0, PREG_SPLIT_NO_EMPTY | PREG_SPLIT_DELIM_CAPTURE);

$splitted = [];


foreach($parts as $key => $part) {
    // preg_split will put delimiters in odd keys, so:
    if ($key % 2 == 1) {
        // Parse header into assoc array
        $h = substr($parts[$key], 3);
        $h = str_replace('"','',$h);
        $h = str_replace('; ','", "',$h);
        $h = '{"' . str_replace(': ','": "',$h) . '"}';
        $h = (array) json_decode($h);
        $name = $h["Name"];

        // Parse type suppressing errors
        $type = @$h["Type"];

        if (!in_array($type, $conf["ignoretypes"])) {
           
            // Parse name
            $name = explode(".", $name)[0];
            $name = explode("(", $name)[0];
            $name = str_replace([ 
                "TABLE ", "VIEW ", "COMMENT ON COLUMN ", "COLUMN ", "EXTENSION ", "FUNCTION " 
            ],'',$name);

            // Parse special types to find their parent object name
            if ($type == "INDEX") {
                $name = strstr(substr(strstr($parts[$key+1], "ON"), 3), " ", true);
            } else if ($type == "CONSTRAINT" || $type == "FK CONSTRAINT") {
                $name = strstr(substr(strstr($parts[$key+1], "ALTER TABLE ONLY"), 17), "\n", true);
            } else if ($type == "RULE") {
                $name = strstr(substr(strstr($parts[$key+1], "TO"), 3), " ", true);
            }
            $name = str_replace('"','',$name);

            // Put content into correct key
            if (empty($splitted[$name])) {
                $splitted[$name] = ["body" => "", "type" => ""];
                $splitted[$name]["body"] = "-- \n" . $parts[$key];
                $addcontent = $parts[$key+1];
            } else {
                $addcontent = "-- \n" . $parts[$key]. $parts[$key+1];
            }
            $splitted[$name]["body"] .= substr($addcontent, 0, -3);

            // Only add defined content types
            if (in_array($type, $conf["savetypes"])) {
                $splitted[$name]["type"] = $type;
            }
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


