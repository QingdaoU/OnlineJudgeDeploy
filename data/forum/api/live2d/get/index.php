<?php
isset($_GET['id']) ? $id = $_GET['id'] : exit('error');

require '../tools/modelList.php';
require '../tools/modelTextures.php';
require '../tools/jsonCompatible.php';

$modelList = new modelList();
$modelTextures = new modelTextures();
$jsonCompatible = new jsonCompatible();

$STATIC_CDN_HOST = getenv('STATIC_CDN_HOST');
if ($STATIC_CDN_HOST) {
    $URL = $STATIC_CDN_HOST.'/api/live2d';
} else {
    $URL = '..';
}

$id = explode('-', $id);
$modelId = (int)$id[0];
$modelTexturesId = isset($id[1]) ? (int)$id[1] : 0;

$modelName = $modelList->id_to_name($modelId);

if (is_array($modelName)) {
    $modelName = $modelTexturesId > 0 ? $modelName[$modelTexturesId-1] : $modelName[0];
    $json = json_decode(file_get_contents('../model/'.$modelName.'/index.json'), 1);
} else {
    $json = json_decode(file_get_contents('../model/'.$modelName.'/index.json'), 1);
    if ($modelTexturesId > 0) {
        $modelTexturesName = $modelTextures->get_name($modelName, $modelTexturesId);
        if (isset($modelTexturesName)) $json['textures'] = is_array($modelTexturesName) ? $modelTexturesName : array($modelTexturesName);
    }
}

$textures = json_encode($json['textures']);
$textures = str_replace('texture', $URL.'/model/'.$modelName.'/texture', $textures);
$textures = str_replace('moc', $URL.'/model/'.$modelName.'/moc', $textures);
$textures = json_decode($textures, 1);
$json['textures'] = $textures;

$json['model'] = $URL.'/model/'.$modelName.'/'.$json['model'];
if (isset($json['pose'])) $json['pose'] = $URL.'/model/'.$modelName.'/'.$json['pose'];
if (isset($json['physics'])) $json['physics'] = $URL.'/model/'.$modelName.'/'.$json['physics'];

if (isset($json['motions'])) {
    $motions = json_encode($json['motions']);
    $motions = str_replace('sounds', $URL.'/model/'.$modelName.'/sounds', $motions);
    $motions = str_replace('snd\/', $URL.'/model/'.$modelName.'/snd/', $motions);
    $motions = str_replace('motions', $URL.'/model/'.$modelName.'/motions', $motions);
    $motions = str_replace('mtn\/', $URL.'/model/'.$modelName.'/mtn/', $motions);
    $motions = json_decode($motions, 1);
    $json['motions'] = $motions;
}

if (isset($json['expressions'])) {
    $expressions = json_encode($json['expressions']);
    $expressions = str_replace('expressions', $URL.'/model/'.$modelName.'/expressions', $expressions);
    $expressions = str_replace('exp\/', $URL.'/model/'.$modelName.'/exp/', $expressions);
    $expressions = json_decode($expressions, 1);
    $json['expressions'] = $expressions;
}

header("Content-type: application/json");
echo $jsonCompatible->json_encode($json);
