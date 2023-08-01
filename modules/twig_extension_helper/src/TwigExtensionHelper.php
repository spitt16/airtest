<?php
namespace Drupal\twig_extension_helper;

use Drupal\twig_extension_helper\model\Announcement;
use Drupal\twig_extension_helper\model\AnnouncementCard;
use Drupal\twig_extension_helper\model\AnnouncementsBand;
use Drupal\twig_extension_helper\model\AnnouncementV2;
use Drupal\twig_extension_helper\model\AnnouncementCollectionV2;
use Drupal\twig_extension_helper\model\AlertV2;
use Drupal\twig_extension_helper\model\AlertCollectionV2;
use Drupal\twig_extension_helper\model\BandContainer;
use Drupal\twig_extension_helper\model\Card;
use Drupal\twig_extension_helper\model\CurrentAQBand;
use Drupal\twig_extension_helper\model\HomeMarquee;
use Drupal\twig_extension_helper\model\LinksCard;
use Drupal\twig_extension_helper\model\ContentBand;
use Drupal\twig_extension_helper\model\LinkImage;
use Drupal\twig_extension_helper\model\Navigation;
use Drupal\twig_extension_helper\model\Band;
use Drupal\twig_extension_helper\model\PublicationsBand;
use Drupal\twig_extension_helper\model\Publication;
use Drupal\twig_extension_helper\model\Partner;
use Drupal\twig_extension_helper\model\PartnersBand;
use Drupal\twig_extension_helper\model\DataProviders;
use Drupal\twig_extension_helper\model\DataProvidersBand;
use Drupal\twig_extension_helper\model\SubpageHeader;
use Drupal\twig_extension_helper\model\TaxonomyVocabulary;
use Drupal\twig_extension_helper\util\NodeUtil;
use Drupal\twig_extension_helper\util\TaxonomyUtil;
use Drupal\twig_extension_helper\util\ParagraphUtil;


class TwigExtensionHelper extends \Twig_Extension {

  /**
   * In this function we can declare the extension function
   */
  public function getFunctions() {
    return array(
      new \Twig_SimpleFunction('constructNavigation',
        array($this, 'constructNavigation'),
        array('is_safe' => array('html'))
      ),
      new \Twig_SimpleFunction('constructHomeMarquee',
        array($this, 'constructHomeMarquee'),
        array('is_safe' => array('html'))
      ),
      new \Twig_SimpleFunction('constructBand',
        array($this, 'constructBand'),
        array('is_safe' => array('html'))
      ),
      new \Twig_SimpleFunction('constructBandContainer',
        array($this, 'constructBandContainer'),
        array('is_safe' => array('html'))
      ),
      new \Twig_SimpleFunction('constructCard',
        array($this, 'constructCard'),
        array('is_safe' => array('html'))
      ),
      new \Twig_SimpleFunction('constructAnnouncement',
        array($this, 'constructAnnouncement'),
        array('is_safe' => array('html'))
      ),
      new \Twig_SimpleFunction('constructAnnouncementV2',
        array($this, 'constructAnnouncementV2'),
        array('is_safe' => array('html'))
      ),
      new \Twig_SimpleFunction('constructAnnouncementCollectionV2',
        array($this, 'constructAnnouncementCollectionV2'),
        array('is_safe' => array('html'))
      ),
      new \Twig_SimpleFunction('constructAlertV2',
        array($this, 'constructAlertV2'),
        array('is_safe' => array('html'))
      ),
      new \Twig_SimpleFunction('constructAlertCollectionV2',
        array($this, 'constructAlertCollectionV2'),
        array('is_safe' => array('html'))
      ),
      new \Twig_SimpleFunction('constructSubpageHeader',
        array($this, 'constructSubpageHeader'),
        array('is_safe' => array('html'))
      ),
      new \Twig_SimpleFunction('constructLinkImage',
        array($this, 'constructLinkImage'),
        array('is_safe' => array('html'))
      ),
      new \Twig_SimpleFunction('getBootstrapColumnCount',
        array($this, 'getBootstrapColumnCount'),
        array('is_safe' => array('html'))
      ),
      new \Twig_SimpleFunction('renderBlock',
        array($this, 'renderBlock'),
        array('is_safe' => array('html'))
      ),
      new \Twig_SimpleFunction('renderNode',
        array($this, 'renderNode'),
        array('is_safe' => array('html'))
      ),
      new \Twig_SimpleFunction('getNodesByType',
        array($this, 'getNodesByType'),
        array('is_safe' => array('html'))
      ),
      new \Twig_SimpleFunction('getTaxonomy',
        array($this, 'getTaxonomy'),
        array('is_safe' => array('html'))
      ),
      new \Twig_SimpleFunction('getTaxonomyTerm',
        array($this, 'getTaxonomyTerm'),
        array('is_safe' => array('html'))
      ),
      new \Twig_SimpleFunction('getTaxonomyTermPublicationByName',
        array($this, 'getTaxonomyTermPublicationByName'),
        array('is_safe' => array('html'))
      ),
      new \Twig_SimpleFunction('getTaxonomyTermPartnerByName',
        array($this, 'getTaxonomyTermPartnerByName'),
        array('is_safe' => array('html'))
      ),
      new \Twig_SimpleFunction('getTaxonomyTermDataProvidersByName',
        array($this, 'getTaxonomyTermDataProvidersByName'),
        array('is_safe' => array('html'))
      )
    );
  }

  public function renderBlock($block_name, $config=null) {
    $block_manager = \Drupal::service('plugin.manager.block');

    if (!isset($config)) {
      $config = [];
    }

    $plugin_block = $block_manager->createInstance($block_name, $config);

    $access_result = $plugin_block->access(\Drupal::currentUser());

    if (is_object($access_result) && $access_result->isForbidden() || is_bool($access_result) && !$access_result) {
      return [];
    }
    $render = $plugin_block->build();

    return $render;
  }

  public function renderNode($nid) {
    $current_node = NodeUtil::nodeLoad($nid);
    $render = \Drupal::entityTypeManager()->getViewBuilder("node")->view($current_node, "default");
    return $render;
  }

  public function constructNavigation($id){
    $current_node = NodeUtil::nodeLoad($id);
    $navigation = new Navigation($current_node);
    return $navigation;
  }

  public function constructBand($current_node) {
    $type = NodeUtil::getBandType($current_node);
	//var_dump($type);exit;
    if($type == "Content") {
      return new ContentBand($current_node);
    } else if ($type == "Publications") {
      return new PublicationsBand($current_node);
    } else if ($type == "Data Providers") {
      return new DataProvidersBand($current_node);
	} else if ($type == "Partners") {
      return new PartnersBand($current_node);
    } else if ($type == "Home Current AQ Data") {
      return new CurrentAQBand($current_node);
    } else if ($type == "Announcements") {
      return new AnnouncementsBand($current_node);
    } else {
      return new Band($current_node);
    }
  }

  public function constructHomeMarquee($current_node) {
    $home_marquee = new HomeMarquee($current_node);
    return $home_marquee;
  }

  public function constructBandContainer($current_node) {
    $band_container = new BandContainer($current_node);
    return $band_container;
  }

  public function constructCard($current_node) {
    $card_type_term = NodeUtil::termLoad($current_node->field_card_type[0]->target_id);
    $card_type_term_label = $card_type_term->label();

    if($card_type_term_label == "Announcement") {
      $card = new AnnouncementCard($current_node);
    } else if ($card_type_term_label == "Links") {
      $card = new LinksCard($current_node);
    } else {
      $card = new Card($current_node);
    }

    return $card;
  }

  public function constructLinkImage($current_node) {
    $link_image = new LinkImage($current_node);
    return $link_image;
  }

  public function constructAnnouncement($current_node) {
    $announcement = new Announcement($current_node);
    return $announcement;
  }

  public function constructAnnouncementV2($current_node) {
    $announcement = new AnnouncementV2($current_node);
    return $announcement;
  }

  public function constructAnnouncementCollectionV2() {
    $nodes = NodeUtil::loadNodesByType("announcement_collection_v2");
    if ($nodes == NULL) {
      return false;
    }
    // Among other things, "reset" returns the value of the first element.
    return new AnnouncementCollectionV2(reset($nodes));
  }

  public function constructAlertV2($current_node) {
    $alert = new AlertV2($current_node);
    return $alert;
  }

  public function constructAlertCollectionV2() {
    $nodes = NodeUtil::loadNodesByType("alert_collection_v2");
    if ($nodes == NULL) {
      return false;
    }
    // Among other things, "reset" returns the value of the first element.
    return new AlertCollectionV2(reset($nodes));
  }

  public function constructSubpageHeader($current_node) {
    $header = new SubpageHeader($current_node);
    return $header;
  }

  public function getBootstrapColumnCount($count) {
    if($count > 0) {
      $bootstrap_calc = 12 / $count;
      if ($bootstrap_calc > 1) {
        return intval(floor($bootstrap_calc));
      }
    }
    return 1;
  }

  public function getTaxonomy($term) {
    return NodeUtil::vocabularyLoad($term);
  }

  public function getTaxonomyTerm($term_id) {
//    $term = NodeUtil::termLoad($term_id);
//    $publications = $term->get("field_");
//    return $publications;
  }

  public function getTaxonomyTermPublicationByName($term_name, $publication_id) {
    $term = NodeUtil::termLoadByName($term_name);

    $publications = ParagraphUtil::getParagraphs($term, "field_publication");
    $publication = null;
    for ($i = 0; $i < count($publications); $i++) {
      $newPublication = new Publication($publications[$i]);
      if ($newPublication->getPublicationId() == $publication_id) {
        $publication = $newPublication;
      }
    }
    return $publication;
  }


 public function getTaxonomyTermPartnerByName($term_name, $partner_id) {
    $term = NodeUtil::termLoadPartnerByName($term_name);

    $partners = ParagraphUtil::getParagraphs($term, "field_partner");
    $partner = null;
    for ($i = 0; $i < count($partners); $i++) {
      $newPartner = new Partner($partners[$i]);
      if ($newPartner->getPartnerId() == $partner_id) {
        $partner = $newPartner;
      }
    }
    return $partner;
  }

public function getTaxonomyTermDataProvidersByName($term_name, $data_provider_id) {
	//var_dump($term_name);
    $term = NodeUtil::termLoadDataProvidersByName($term_name);
    //var_dump($term);
    $data_providers = ParagraphUtil::getParagraphs($term, "field_data_provider");
    $data_provider = null;
    for ($i = 0; $i < count($data_providers); $i++) {
      $newDataProviders = new DataProviders($data_providers[$i]);
      if ($newDataProviders->getDataProvidersId() == $data_provider_id) {
        $data_provider = $newDataProviders;
      }
    }
    return $data_provider;
  }
}
