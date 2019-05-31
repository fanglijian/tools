<?php

function usage() {
    echo "php gen_sql.php <file>\n";
}

if ($argc != 2) {
    usage();
    exit;
}

$fp = $argv[1];
if (!file_exists($fp)) {
    usage();
    exit;
}

$handle = fopen($fp, 'r');
if ($handle) {
    $keys = array();
    $values = array();
    $sql = "";
    $table = "";
    $where = "";
    $insert = true;
    while (($line = fgets($handle)) !== false) {
        if (strlen($line) == 0) {
            continue;
        }
        if ($line[0] != ' ') {
            if (!empty($sql)) {
                if ($insert) {
                    for ($i = 0; $i < count($keys); ++$i) {
                        if ($i != 0) {
                            $sql .= ', ';
                        }
                        $sql .= '`'.$keys[$i].'`';
                    }
                    $sql .= ' ) VALUES ( ';
                    for ($i = 0; $i < count($values); ++$i) {
                        if ($i != 0) {
                            $sql .= ', ';
                        }
                        if ($values[$i] == '') {
                            $sql .= '\'\'';
                        } else if ($values[$i] != null) {
                            $sql .= '\''.$values[$i].'\'';                                
                        } else {
                            $sql .= 'null';                                                            
                        }
                    }
                    $sql .= ' );';                    
                } else {
                    for ($i = 0; $i < count($keys); ++$i) {
                        if ($i != 0) {
                            $sql .= ', ';
                        }
                        $v = $values[$i];
                        if ($v[0] == '+') {
                            $sql .= '`'.$keys[$i].'`=`'.$keys[$i].'`'.substr($v, 1);
                        } else {
                            $sql .= '`'.$keys[$i].'`=\''.$values[$i].'\'';
                        }

                    }
                    $sql .= $where;
                }
                echo $sql."\n\n";
                $keys = array();
                $values = array();
                $sql = "";
                $table = "";
                $where = "";
            }
            $line = trim($line);
            $pos = strpos($line, '.');
            if ($pos !== false) {
                $insert = false;
                $sql = 'UPDATE `'.substr($line, 0, $pos).'` SET ';
                $where = ' WHERE `id`=\''.substr($line, $pos+1).'\';';
            } else {
                $insert = true;                
                $sql = 'INSERT INTO `'.$line.'` ( ';
            }
        } else {
            $line = trim($line);
            $pos = strpos($line, '=');
            if ($pos !== false) {
                $keys[] = substr($line, 0, $pos);
                $v = substr($line, $pos+1);
                if ($v === false) {
                    $v = '';
                } else if ($v == '%00%') {
                    $v = null;
                }
                $values[] = $v;
            } else {
                $pos = strpos($line, '+');
                if ($pos !== false) {
                    $keys[] = substr($line, 0, $pos);
                    $values[] = '+'.substr($line, $pos+1);
                }
            }
        }
    }
    if (!empty($sql)) {
        if ($insert) {
            for ($i = 0; $i < count($keys); ++$i) {
                if ($i != 0) {
                    $sql .= ', ';
                }
                $sql .= '`'.$keys[$i].'`';
            }
            $sql .= ' ) VALUES ( ';
            for ($i = 0; $i < count($values); ++$i) {
                if ($i != 0) {
                    $sql .= ', ';
                }
                if ($values[$i] == '') {
                    $sql .= '\'\'';
                } else if ($values[$i] != null) {
                    $sql .= '\''.$values[$i].'\'';                                
                } else {
                    $sql .= 'null';                                                            
                }
            }
            $sql .= ' );';                    
        } else {
            for ($i = 0; $i < count($keys); ++$i) {
                if ($i != 0) {
                    $sql .= ', ';
                }
                $v = $values[$i];
                if ($v[0] == '+') {
                    $sql .= '`'.$keys[$i].'`=`'.$keys[$i].'`'.substr($v, 1);
                } else {
                    $sql .= '`'.$keys[$i].'`=\''.$values[$i].'\'';
                }

            }
            $sql .= $where;
        }
        echo $sql."\n";
    }
    fclose($handle);
} else {
    echo "Error processing file, exit\n";
}
    
    
?>