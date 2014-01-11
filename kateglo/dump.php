<?php
/**
 * Generate tagged lexicon from Kateglo
 * DET not tagged
 */
include_once('config.php');
require_once('vendor/autoload.php');

$mapping = array(
    'adj'   => 'ADJ',
    'adv'   => 'ADV',
    'i'     => 'PRT', // interjection, not sure where to put it
    'k'     => 'CONJ',
    'l'     => 'PRT',
    'n'     => 'NOUN',
    'num'   => 'NUM',
    'pre'   => 'ADP',
    'pron'  => 'PRON',
    'v'     => 'VERB'
);
// open file
$file = 'lexicon-id-kateglo.json';
$fp = fopen($file, 'w');

// get lemma
$db = \Doctrine\DBAL\DriverManager::getConnection($DB_PARAM);
$qb = $db->createQueryBuilder();
$qb
    ->select('phrase, lex_class')
    ->from('phrase', 'p')
    ->where('actual_phrase IS NULL AND lex_class <> \'bt\'')
    ->groupBy('phrase')
    ->orderBy('phrase');
$stmt = $qb->execute();
fwrite($fp, "{\n");
$started = false;
while ($row = $stmt->fetch()) {
    $phrase = $row['phrase'];
    echo($phrase . "\n"); // indicate progress
    $lexicon[$phrase] = array();
    if ($mapping[$row['lex_class']]) {
        $lexicon[$phrase][] = $mapping[$row['lex_class']];
    }
    // get class from definition
    $sql2 = "SELECT lex_class FROM definition " .
        "WHERE phrase = ? AND lex_class IS NOT NULL";
    $stmt2 = $db->prepare($sql2);
    $stmt2->bindValue(1, $row['phrase']);
    $stmt2->execute();
    $class2 = $stmt2->fetchAll();
    // push class from definition
    if (count($class2) > 0) {
        foreach ($class2 as $class) {
            if (!in_array($mapping[$class['lex_class']], $lexicon[$phrase])) {
                $lexicon[$phrase][] = $mapping[$class['lex_class']];
            }
        }
    }
    if (!$started) {
        $started = true;
    } else {
        fwrite($fp, ",\n");
    }
    fwrite($fp, "\t\"" . $phrase . '": ["' . implode('", "', $lexicon[$phrase]) . '"]');
}

// close file
fwrite($fp, "\n}");
fclose($fp);
