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
use Drupal\twig_extension_helper\model\Publication;

class PublicationsBand extends Band {
  var $term_parent = NULL,
      $id = NULL,
      $related_terms = [],
      $publications = [];

  function __construct($node_obj) {
    parent::__construct($node_obj);
    $this->id = $node_obj->field_band_publications_type[0]->target_id;
    $publications = [];
    if(!is_null($node_obj->field_band_publications_type[0])) {
      $parent = \Drupal::entityTypeManager()->getStorage('taxonomy_term')->loadParents($node_obj->field_band_publications_type[0]->target_id);
      foreach ($parent as $p) {
        $this->term_parent = $p;
      }

      $vocab = new Vocabulary("publications");

      foreach ($vocab->getValue() as $term) {
        if ($term->tid == $this->term_parent->id()) {
          $childrenArray = $term->children;
          foreach ($childrenArray as $child) {
            array_push($this->related_terms, $child);
          }
        }
      }

      $term = NodeUtil::termLoad($node_obj->field_band_publications_type[0]->target_id);
      $publications = ParagraphUtil::getParagraphs($term, "field_publication");
    }

    foreach ($publications as $publication) {
      array_push($this->publications, new Publication($publication));
    }

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
  public function getPublications()
  {
    return $this->publications;
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
  public function getPublicationsForTermId($termId)
  {
    $publicationsList = [];
    $term = NodeUtil::termLoad($termId);
    $publications = ParagraphUtil::getParagraphs($term, "field_publication");
    /** AirNowDrupal Issue 2: Less Detail on right side list on publications page cw 2018-03-27
	foreach ($publications as $publication) {
      array_push($publicationsList, new Publication($publication));
    }
	**/
    return $publicationsList; 
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
