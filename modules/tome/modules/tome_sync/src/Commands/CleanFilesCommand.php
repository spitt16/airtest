<?php

namespace Drupal\tome_sync\Commands;

use Drupal\Core\Config\StorageInterface;
use Drupal\tome_base\CommandBase;
use Drupal\tome_base\PathTrait;
use Drupal\tome_sync\ContentIndexerTrait;
use Drupal\tome_sync\FileTrait;
use Drupal\tome_sync\TomeSyncHelper;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;

/**
 * Contains the tome:clean-files command.
 *
 * @internal
 */
class CleanFilesCommand extends CommandBase {

  use FileTrait;
  use PathTrait;
  use ContentIndexerTrait;

  /**
   * The target content storage.
   *
   * @var \Drupal\Core\Config\StorageInterface
   */
  protected $contentStorage;

  /**
   * The config storage.
   *
   * @var \Drupal\Core\Config\StorageInterface
   */
  protected $configStorage;

  /**
   * Creates a CleanFilesCommand object.
   *
   * @param \Drupal\Core\Config\StorageInterface $content_storage
   *   The target content storage.
   * @param \Drupal\Core\Config\StorageInterface $config_storage
   *   The target config storage.
   */
  public function __construct(StorageInterface $content_storage, StorageInterface $config_storage) {
    parent::__construct();
    $this->contentStorage = $content_storage;
    $this->configStorage = $config_storage;
  }

  /**
   * {@inheritdoc}
   */
  protected function configure() {
    $this->setName('tome:clean-files')
      ->setDescription('Deletes unused files.');
  }

  /**
   * {@inheritdoc}
   */
  protected function execute(InputInterface $input, OutputInterface $output) {
    $this->io()->writeLn('Searching for unused files...');
    $files = $this->getUnusedFiles();
    if (empty($files)) {
      $this->io()->success('No unused files found.');
      return 0;
    }
    $this->io()->listing($files);
    if (!$this->io()->confirm('The files listed above will be deleted.', FALSE)) {
      return 0;
    }
    $file_directory = $this->getFileDirectory();
    foreach ($files as $uuid => $filename) {
      $this->contentStorage->delete("file.$uuid");
      $this->unIndexContentByName("file.$uuid");
      file_unmanaged_delete($this->joinPaths($file_directory, $filename));
    }
    $this->io()->success('Deleted all unused files.');
  }

  /**
   * Assembles a list of files that should be unused.
   *
   * @return array
   *   An associative array mapping file UUIDs to their URIs.
   */
  protected function getUnusedFiles() {
    $files = [];
    $names = $this->contentStorage->listAll('file.');
    foreach ($names as $name) {
      $data = $this->contentStorage->read($name);
      list(, $uuid) = TomeSyncHelper::getPartsFromContentName($name);
      $files[$uuid] = file_uri_target($data['uri'][0]['value']);
    }
    $callback = function ($value) use (&$files) {
      if (is_string($value)) {
        foreach ($files as $uuid => $filename) {
          if (strpos($value, $uuid) !== FALSE || strpos($value, $filename) !== FALSE) {
            unset($files[$uuid]);
          }
        }
      }
    };
    $names = array_diff($this->contentStorage->listAll(), $names);
    foreach ($names as $name) {
      if (!$files) {
        break;
      }
      $data = $this->contentStorage->read($name);
      array_walk_recursive($data, $callback);
    }
    $names = $this->configStorage->listAll();
    foreach ($names as $name) {
      if (!$files) {
        break;
      }
      $data = $this->configStorage->read($name);
      array_walk_recursive($data, $callback);
    }
    return $files;
  }

}
