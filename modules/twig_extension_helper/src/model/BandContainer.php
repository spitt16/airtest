<?php
/**
 * Created by IntelliJ IDEA.
 * User: sdave
 * Date: 2/14/2018
 * Time: 9:24 AM
 */

namespace Drupal\twig_extension_helper\model;


use Drupal\twig_extension_helper\util\ModelUtil;
use Drupal\twig_extension_helper\util\NodeUtil;

class BandContainer {
  var $nid,
      $title,
      $band_reference = NULL,
      $band_reference_nids = [],
      $parent_type = NULL,
      $display_type = NULL;

  function __construct($node_obj, $load_bands=false) {
    $this->nid = $node_obj->nid[0]->value;

    if(!ModelUtil::isFirstNull($node_obj->field_title)) {
      $this->title = $node_obj->field_title[0]->value;
    }



    foreach($node_obj->field_band_references as $current_band_reference) {
      array_push($this->band_reference_nids, $current_band_reference->target_id);
    }

    if($load_bands) {
      $this->band_reference = [];
      foreach($node_obj->field_band_references as $current_band_reference) {
        $current_band = new ContentBand(NodeUtil::nodeLoad($current_band_reference->target_id));
        array_push($this->band_reference, $current_band);
      }
    }

    $band_container_type_term = NodeUtil::termLoad($node_obj->field_band_container_display[0]->target_id);
    $this->display_type = $band_container_type_term->label();
  }

  /**
   * @return mixed
   */
  public function getNid() {
    return $this->nid;
  }

  /**
   * @return mixed
   */
  public function getTitle() {
    return $this->title;
  }

  /**
   * @return array|null
   */
  public function getBandReference() {
    return $this->band_reference;
  }

  /**
   * @return array
   */
  public function getBandReferenceNids() {
    return $this->band_reference_nids;
  }

  /**
   * @return null
   */
  public function getParentType() {
    return $this->parent_type;
  }

  /**
   * @return null
   */
  public function getDisplayType() {
    return $this->display_type;
  }


}
