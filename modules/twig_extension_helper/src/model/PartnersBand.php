<?php
/**
 * Created by IntelliJ IDEA.
 * User: sdave
 * Date: 2/14/2018
 * Time: 9:20 AM
 */

namespace Drupal\twig_extension_helper\model;


use Drupal\twig_extension_helper\util\ParagraphUtil;
use Drupal\twig_extension_helper\util\NodeUtil;
use Drupal\twig_extension_helper\util\ModelUtil;
use Drupal\twig_extension_helper\model\Partner;


class PartnersBand extends Band {
  var $term_parent = NULL,
	  $term_children = NULL,
	  $thisTerm = NULL,
      $id = NULL,
      $related_terms = [],
      $partners = [];

  function __construct($node_obj) {
    parent::__construct($node_obj);
    $this->id = $node_obj->field_band_partners_type[0]->target_id;
    $partners = [];
    if(!is_null($node_obj->field_band_partners_type[0])) {
      $parent = \Drupal::entityTypeManager()->getStorage('taxonomy_term')->loadParents($node_obj->field_band_partners_type[0]->target_id);
      foreach ($parent as $p) {
        $this->term_parent = $p;
      }
      $vocab = new Vocabulary("Partners");

      foreach ($vocab->getValue() as $term) {
        if ($term->tid == $this->term_parent->id()) {
          $childrenArray = $term->children;
          foreach ($childrenArray as $child) {
            array_push($this->related_terms, $child);
          }
        }
      }

      $term = NodeUtil::termLoad($node_obj->field_band_partners_type[0]->target_id);
      $partners = ParagraphUtil::getParagraphs($term, "field_partner");
    }

    foreach ($partners as $partner) {
      array_push($this->partners, new partner($partner));
    }

  }

  /**
   * @return NULL
   */
  public function getTermChildren($termId) {
	$children = [];
	$vocabulary_entities = [];
    //$vocab = new Vocabulary($thisTerm);

	$term = NodeUtil::termLoad($termId);
	//$vocabulary_entities = \Drupal::entityTypeManager()->getStorage('taxonomy_term')->loadTree(234, 0, NULL, TRUE);
	$children = \Drupal::entityTypeManager()->getStorage('taxonomy_term')->loadChildren($term->tid);


	//$children = $this->entityTypeManager->getStorage('taxonomy_term')->loadChildren($node_obj->field_band_partners_type[0]->target_id);

	//$childrenArray = $term->children;
	//	  foreach ($childrenArray as $child) {
	// 	array_push($this->term_children, $child);
	// 	}

  return $children;

	 // $vocab = new Vocabulary($thisTerm);
	 // foreach ($vocab->getValue() as $term) {

	//	  $children = $this->entityTypeManager->getStorage($term)->loadChildren($object->tid);
	//
	//	  $childrenArray = $term->children;
	//	  foreach ($childrenArray as $child) {
	//		array_push($this->term_children, $child);
	//	  }

//	  }
	//  return $this->term_children;
  }




	/**
   * @return NULL
   */
  public function getTermParent() {
    return $this->term_parent;
  }

  /**
   * @return array
   */
  public function getPartners()
  {
    return $this->partners;
  }

  /**
   * @return array|Vocabulary
   */
  public function getRelatedTerms()
  {
    return $this->related_terms;
  }

  /**
   * @return NULL
   */
  public function getTid()
  {
    return $this->id;
  }

  /**
   * @return NULL
   */
  public function getFormattedPath($name)
  {
    return ModelUtil::stringToCleanPath($name);
  }

  /**
   * @return array
   */
  public function getPartnersForTermId($termId)
  {
    $partnersList = [];
    $term = NodeUtil::termLoad($termId);
    $partners = ParagraphUtil::getParagraphs($term, "field_partner");

	  foreach ($partners as $partner) {
      array_push($partnersList, new partner($partner));
    }

    return $partnersList;
  }

  /**
   * @return NULL
   */
  public function getUrlAliasForTermId($termId)
  {
    $aliasManager = \Drupal::service('path.alias_manager');
    // The second argument to getAliasByPath is a language code such as "en" or LanguageInterface::DEFAULT_LANGUAGE.
    $alias = $aliasManager->getAliasByPath('/taxonomy/term/' . $termId);
    return $alias;
  }


}
