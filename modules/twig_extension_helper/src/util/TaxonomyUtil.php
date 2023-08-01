<?php
/**
 * Created by IntelliJ IDEA.
 * User: sdave
 * Date: 1/16/2018
 * Time: 10:27 AM
 */

namespace Drupal\twig_extension_helper\util;


use Drupal\taxonomy\Entity\Term;

class TaxonomyUtil {
  public static function vocabularyTreeLoad($entity_manager, $vocabulary_name, $tid=NULL) {
    if(!is_null($entity_manager)) {
      if(is_null($tid)) {
        return $entity_manager
          ->getStorage('taxonomy_term')
          ->loadTree($vocabulary_name);
      } else {
        return $entity_manager
          ->getStorage('taxonomy_term')
          ->loadTree($vocabulary_name, $tid);
      }
    }
  }

  public static function vocabularyChildrenLoad($entity_manager, $vocabulary_children_name) {
    if(!is_null($entity_manager)) {
      return $entity_manager->getStorage('taxonomy_term')
        ->loadChildren($vocabulary_children_name);
    }
  }

  public static function vocabularyFieldLoad($entity_manager, $tid, $field_name) {
      if(!is_null($entity_manager)) {
        return $entity_manager->getStorage('taxonomy_term')
          ->load($tid)
          ->get($field_name);
      }
  }

  public static function termLoad($entity_manager, $tid) {
    if(!is_null($entity_manager)) {
      return $entity_manager->getStorage('taxonomy_term')
        ->load($tid);
    }
  }

//  public static function termLoadByName($entity_manager, $term_name, $vid=NULL) {
////    if(!is_null($entity_manager)) {
////      $properties = [];
////      if (!empty($name)) {
////        $properties['name'] = $term_name;
////      }
////      if (!empty($vid)) {
////        $properties['vid'] = $vid;
////      }
////      $terms = $entity_manager->getStorage('taxonomy_term')
////        ->loadByProperties($properties);
////      $term = reset($terms);
////    }
////    return !empty($term) ? $term->id() : 0;
//    $term_matches = taxonomy_term_load_multiple_by_name($term_name, "publications");
//    $term = null;
//    if (count($term_matches) > 0) {
//      $term = array_pop($term_matches);
//    }
//
//    $term_id = $term->id();
//
//
//
//    return $term->id();
//
//  }
}
