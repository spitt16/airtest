<?php
/**
 * Created by IntelliJ IDEA.
 * User: sdave
 * Date: 3/2/2018
 * Time: 2:22 PM
 */

namespace Drupal\twig_extension_helper\model;

use Drupal\twig_extension_helper\util\ParagraphUtil;
use Drupal\twig_extension_helper\util\TaxonomyUtil;
use Drupal\twig_extension_helper\util\TruncateHTML;
use Drupal\twig_extension_helper\util\NodeUtil;

class StatusMessageTerm extends VocabularyTerm {
  var $term, $publish, $hasChild = 0, $hasParent = 0, $url_first = NULL, $url_state = NULL, $state = NULL,
	  $archive, $display_more_link, $custom_more_link, $path_default = NULL, $datetime, $title, $summary;

   public function __construct($object) {
     parent::__construct($object);   
	   
     $current_tid = $this->tid;
     $this->term = TaxonomyUtil::termLoad($this->entity_manager, $current_tid);
	   //var_dump("<pre>");
	   //var_dump($this->term);	   
	$this->publish = $this->vocabularyFieldLoad($current_tid, "field_status_publish")->getValue()[0]['value'];
	//var_dump((($this->tid)));  
	   
	// IF on a State-level page, THEN only display state-level alerts, ELSE display non-state level alerts
	// cw 2018-07-26
	//var_dump($this->tid);
	   
	// Read URL to find is State Page is being requestted.
	$url = $_SERVER['REQUEST_URI'];
    //var_dump(parse_url($url, PHP_URL_PATH));
	$urlParts = explode("/", parse_url($url, PHP_URL_PATH) ); // Parse the URL
	if(count($urlParts) > 2) {
	   $this->url_first = $urlParts[1];   // First part of the URL after the server name
	   $this->url_state = $urlParts[2];   // State name part of the URL after the server name
	   };     
	 //var_dump($this->url_state);
	   
	// Check for possible Childern; If the term has Children then it's a State LABEL
	$childern = \Drupal::entityTypeManager()->getStorage('taxonomy_term')->loadChildren($this->tid);
	foreach($childern as $child) {
		//$childTerm = $child->get('tid')->value;
		$this->hasChild = 1;
		}
		//var_dump($this->hasChild);
	// Check for possible Childern; If the term has a Parent then it's a State-level alert   
	$parents = \Drupal::entityTypeManager()->getStorage('taxonomy_term')->loadParents($this->tid);  
	   foreach($parents as $parent) {
		$this->hasParent = 1;
		//var_dump($parent->id());
		$this->state = strtolower($this->vocabularyFieldLoad($parent->id(), "name")->getValue()[0]['value']);   
		//var_dump($this->state);
		}
	   
	 // ONLY Published and top-level alerts; and state-level Alerts on the State Level ONLY  
	if($this->url_first == "state")  {
		// State level alert
		if($this->publish and $this->hasParent) {
			if($this->url_state == $this->state) {
				$this->summary = $this->vocabularyFieldLoad($current_tid, "field_status_summary")->getValue()[0]['value'];
			}
		}
	} else {
		// Non-state level alert
		if($this->publish and !$this->hasChild and !$this->hasParent) {
	     	$this->summary = $this->vocabularyFieldLoad($current_tid, "field_status_summary")->getValue()[0]['value'];
		   	//var_dump($this->publish);
		 	//var_dump($this->summary);
    		}
	}
      //     $this->body = $this->vocabularyFieldLoad($current_tid, "field_status_body")->getValue()[0]['value'];
     //$this->display_more_link = boolval($this->vocabularyFieldLoad($current_tid, "field_status_display_more_link")->getValue()[0]['value']);
     //$this->custom_more_link = new Link(ParagraphUtil::getParagraphs(TaxonomyUtil::termLoad($this->entity_manager, $current_tid), "field_more_link")[0]);
    // $temp_path_default = $this->vocabularyFieldLoad($current_tid, "field_status_path_default")->getValue();
    // if(count($temp_path_default) > 0) {
    //  $this->path_default = $temp_path_default[0]['value'];
    // }
   }

  /**
   * @return mixed
   */
  public function getSummary() {   
	// AirNowDrupal # 132 Check the non-presistant cookie "dismisStatusMessage"  
    if(isset($_COOKIE["statusMessageDismiss"])) {
		//var_dump("here");
		//var_dump(isset($_COOKIE["statusMessageDismiss"]));
		// clear out the alert messages so that they are not returned cw 2019-05-24
		//$this->summary = NULL;
		}
	  return $this->summary;
  }

  public function getMobileSummary() {
//    return $this->getSubstrSummary(35);
    return TruncateHTML::truncateChars(trim($this->getSummary()), 35);
  }

  public function getTabletSummary() {
//    return $this->getSubstrSummary(53);
    return TruncateHTML::truncateChars(trim($this->getSummary()), 53);
  }

  public function getSubstrSummary($cutoff) {
    $current_summary = trim($this->getSummary());

    if(strlen($current_summary) > $cutoff) {
      $current_table_summary = substr($current_summary, 0, $cutoff - 1);
      return trim($current_table_summary)  . "...";
    } else {
      return $current_summary;
    }
  }
  /**
   * @return mixed
   */
  public function getBody() {
    return $this->body;
  }

  /**
   * @return mixed
   */
  public function getPublish() {
    return $this->publish;
  }

  /**
   * @return mixed
   */
  public function getArchive() {
    return $this->archive;
  }

  /**
   * @return mixed
   */
  public function getDatetime() {
    return $this->datetime;
  }

  /**
   * @return mixed
   */
  public function getPathDefault() {
    return $this->path_default;
  }

  /**
   * @return mixed
   */
  public function getDisplayMoreLink() {
    return $this->display_more_link;
  }

  /**
   * @return mixed
   */
  public function getCustomMoreLink() {
    return $this->custom_more_link;
  }



}
