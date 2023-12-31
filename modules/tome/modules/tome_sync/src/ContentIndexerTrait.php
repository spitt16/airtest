<?php

namespace Drupal\tome_sync;

use Drupal\Core\Entity\ContentEntityInterface;
use Drupal\Core\Field\EntityReferenceFieldItemListInterface;
use Drupal\Core\Site\Settings;

/**
 * Provides methods for reading and writing the index file.
 *
 * @todo Move to a service?
 *
 * @internal
 */
trait ContentIndexerTrait {

  /**
   * Writes content to the index.
   *
   * @param \Drupal\Core\Entity\ContentEntityInterface $entity
   *   An entity to be indexed.
   */
  protected function indexContent(ContentEntityInterface $entity) {
    $dependencies = [];
    foreach ($entity as $field) {
      if ($field instanceof EntityReferenceFieldItemListInterface) {
        foreach ($field->referencedEntities() as $referenced_entity) {
          if ($referenced_entity instanceof ContentEntityInterface) {
            $dependencies[] = TomeSyncHelper::getContentName($referenced_entity);
          }
        }
      }
    }
    if (!$entity->isDefaultTranslation()) {
      $dependencies[] = TomeSyncHelper::getContentNameFromParts($entity->getEntityTypeId(), $entity->uuid());
    }
    $handle = $this->acquireContentIndexLock();
    $contents = stream_get_contents($handle);
    if (empty($contents)) {
      $index = [];
    }
    else {
      $index = json_decode($contents, TRUE);
    }
    $dependencies = array_values(array_unique($dependencies));
    $index[TomeSyncHelper::getContentName($entity)] = $dependencies;
    ftruncate($handle, 0);
    rewind($handle);
    fwrite($handle, json_encode($index, JSON_PRETTY_PRINT));

    flock($handle, LOCK_UN);
  }

  /**
   * Removes content from the index.
   *
   * @param \Drupal\Core\Entity\ContentEntityInterface $entity
   *   An entity to be indexed.
   */
  protected function unIndexContent(ContentEntityInterface $entity) {
    $name = TomeSyncHelper::getContentName($entity);
    $this->unIndexContentByName($name);
  }

  /**
   * Removes content from the index.
   *
   * @param string $name
   *   A content name.
   */
  protected function unIndexContentByName($name) {
    $handle = $this->acquireContentIndexLock();
    $contents = stream_get_contents($handle);
    if (empty($contents)) {
      return;
    }
    $index = json_decode($contents, TRUE);
    if (isset($index[$name])) {
      unset($index[$name]);
    }
    foreach ($index as &$dependencies) {
      $dependencies = array_diff($dependencies, [$name]);
    }
    ftruncate($handle, 0);
    rewind($handle);
    fwrite($handle, json_encode($index, JSON_PRETTY_PRINT));

    flock($handle, LOCK_UN);
  }

  /**
   * Acquires a lock for writing to the index.
   *
   * @return resource
   *   A file pointer resource on success.
   *
   * @throws \Exception
   *   Throws an exception when the index file cannot be written to.
   */
  protected function acquireContentIndexLock() {
    $destination = $this->getContentIndexFilePath();
    $directory = dirname($destination);
    file_prepare_directory($directory, FILE_CREATE_DIRECTORY);
    $handle = fopen($destination, 'c+');
    if (!flock($handle, LOCK_EX)) {
      throw new \Exception('Unable to acquire lock for the index file.');
    }
    return $handle;
  }

  /**
   * Gets the contents of the index.
   *
   * @return bool|array
   *   The index, or FALSE if there was an error.
   */
  protected function getContentIndex() {
    $destination = $this->getContentIndexFilePath();
    if (!file_exists($destination)) {
      return FALSE;
    }
    $contents = file_get_contents($destination);
    return json_decode($contents, TRUE);
  }

  /**
   * Deletes the index file.
   */
  protected function deleteContentIndex() {
    $destination = $this->getContentIndexFilePath();
    if (is_file($destination)) {
      unlink($destination);
    }
  }

  /**
   * Gets the index file path.
   *
   * @return string
   *   The index file path.
   */
  protected function getContentIndexFilePath() {
    return Settings::get('tome_content_directory', '../content') . '/meta/index.json';
  }

}
