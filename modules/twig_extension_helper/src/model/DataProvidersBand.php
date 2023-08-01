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
use Drupal\twig_extension_helper\model\DataProviders;
use Drupal\twig_extension_helper\model\Partner;

class DataProvidersBand extends Band {
 var $data_provider_name = NULL,
	 $data_provider_code = NULL,
	 $urlParts = [],
	 $reporting_area_name = NULL,
	  $term_parent = NULL,
	  $term_children = NULL,
	  $thisTerm = NULL,
	  $name = NULL,
      $tid = NULL,
	  $id = NULL,
      $related_terms = [],
	  $partner_term = NULL,
	  $description = NULL,
      $data_providers = [];

  function __construct($node_obj) {
     parent::__construct($node_obj);
	 $this->id = $node_obj->field_band_data_providers_type[0]->target_id;
	  //var_dump($this);
	 // Read URL to find the Reporting Area being requestted.
	 $url = $_SERVER['REQUEST_URI'];
     //var_dump(parse_url($url, PHP_URL_PATH));
	 $urlParts = explode("/", parse_url($url, PHP_URL_PATH) ); // Parse the URL
	  if(count($urlParts) > 2) {
		$this->data_provider_code = $urlParts[2];   // strip off the Reporting
	 	}; 
	 //var_dump( $this->data_provider_code);var_dump("<P><p>");
	 
	 if(!is_null($this->data_provider_code)) {	
     	// If a Repaorting Area value was passed, then look it up! 
		 
         $vocab = new Vocabulary("data_providers");
		 
      	 // dig down the Taxonomy to find the given Reporting Area
		 foreach ($vocab->getValue() as $term) { 
			  $children = $term->children;
			  foreach ($children as $child) {
				  $grandchildren = $child->children;
				  // Pull values from this grandChild term
				  foreach ($grandchildren as $grandChild) { 				  
					  // Check for match with URL value
					  if($this->getReportingAreaIdForTermId($grandChild->tid) == $this->data_provider_code ) {
							// Hit!
							//var_dump($this->getReportingAreaIdForTermId($grandChild->tid) );var_dump("<- This one<P><p>"); //var_dump($this);exit;
						    //var_dump($this->getDataProvidersForTermId($grandChild->tid) );var_dump("<- has these Data Providers<P><p>");
						  	$this->reporting_area_name = $grandChild->name; 
						  	$this->data_providers = $this->getDataProvidersForTermId($grandChild->tid);
							//var_dump($grandChild);var_dump("<P><p>"); // working here... 2018-07-05  
					  		}
					  }
				  }   
			   }
        	//$term = NodeUtil::termLoad($node_obj->field_band_data_providers_type[0]->target_id);
		 // Show the Data Providers
			//var_dump("<pre>");
		 	//var_dump($this->data_providers);
		    //var_dump("</pre>");
    }
	   $term = NodeUtil::termLoad($node_obj->field_band_data_providers_type[0]->target_id);

   } // END function _construct
	
   /**
   * Returns the Dataproviders for this Reporting Area
   * cw 2018-07-05
   */
  public function getDataProviders()
  {
    return $this->data_providers;
  }
   /**
   * Returns the Reporting Area ID
   * cw 2018-07-11
   */
  public function getReportingAreaId()
  {
    return $this->data_provider_code;
  }
   /**
   * Returns the Reporting Area Name
   * cw 2018-07-11
   */
  public function getReportingAreaName()
  {
    return $this->reporting_area_name;
  }

  /**
   * Returns the Data Provider Name for a Given TermID
   * cw 2018-07-11
   */
  public function getDataProviderName($termId)
  {
    // Pull the Data Provider Term for this term ID
	$term = NodeUtil::termLoad($termId);
	// Pull the Name
	$this->data_provider_name = $term->name[0]->value;
	  
	return $this->data_provider_name;
  }

	/**
   * Returns Partner URL for a given Partner Term ID
   */
  public function getPartnerUrlForTermId($termId)
  {
    $partnersList = [];
    $term = NodeUtil::termLoad($termId);
    $partners = ParagraphUtil::getParagraphs($term, "field_partner");
   
	foreach ($partners as $partner) {
      array_push($partnersList, new partner($partner));
    }
	
	$this->data_provider_url = $partnersList[0]->partner_url;
    
	 // var_dump("<pre>");
	 // var_dump($this->data_provider_url);
	 // var_dump("</pre><P>");exit;
	
    return $this->data_provider_url; 
  }
	


	
  /**
   * @return array|Vocabulary
   */
  public function getGrandChildren()
  {
    return $this->grandChildren;
  }

  /**
   * @return NULL
   */
  public function getTid()
  {
    return $this->tid;
  }
	  /**
   * Returns ID value for the Data Providers Type
   */
  public function getid()
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
   * Returns the Reporting Area ID value for the given term
   * cw 2018-07-05
   */
  public function getReportingAreaIdForTermId($termId)
  {
    $term = NodeUtil::termLoad($termId);
	  // Debug area  cw 2018-07-27
	  //var_dump("<pre>");var_dump($term);var_dump("<br>");
	  //var_dump("<p><p>");
	  //var_dump($term->name[0]->value);
	  // exit;
	
	// Check for missing Reporting Area ID; Issue #14  cw 2018-07-27
    if(!is_null($term->field_reporting_area_id[0])) {
		$reportingAreaId = $term->field_reporting_area_id[0]->value;
	} else {
		// Missing! Handle it and write to the Log
		$reportingAreaId = " ";
		$message = "{$term->name[0]->value} ({$termId}) is missing a Reporting Area ID.";
		\Drupal::logger('Data-Providers')->notice($message);
	}
			
    return $reportingAreaId; 
  }
	
	 /**
   * Returns the Data Providers for the given term
   * cw 2018-07-05
   */
  public function getDataProvidersForTermId($termId)
  {
    $dataProvidersList = [];
    $term = NodeUtil::termLoad($termId);
	 // var_dump($termId);exit;
    $dataProviders = ParagraphUtil::getParagraphs($term, "field_data_provider");
   
	foreach ($dataProviders as $dataProvider) {
	  //var_dump($dataProvider->id[0]->value);var_dump("<P><p>");
      array_push($dataProvidersList, $dataProvider->id[0]->value);
    }
	
    return $dataProvidersList; 
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