<?php
  namespace Drupal\twig_extension_helper\util;
  use Drupal;
  use Drupal\node\Entity\Node;
  use Drupal\taxonomy\Entity\Term;
  use Drupal\twig_extension_helper\model\Publication;
  use Drupal\twig_extension_helper\model\Partner;
  use Drupal\twig_extension_helper\model\DataProviders;

  class NodeUtil {
    public static function nodeLoad($id) {
      return Node::load($id);
    }

    public static function termLoad($id) {
      return Term::load($id);
    }

    public static function loadNodesByType($node_type) {
      $nids = Drupal::entityQuery('node')->condition('type', $node_type)->execute();
      $nodes = Node::loadMultiple($nids);
      return $nodes;
    }

    public static function termLoadByName($term_name) {
      $clean_name = str_replace('-', ' ', strtolower($term_name));
      $term_matches = taxonomy_term_load_multiple_by_name($clean_name, "publications");
      $term = null;
      if (count($term_matches) > 0) {
        $term = array_pop($term_matches);
      }
      return $term;
//      $publications = ParagraphUtil::getParagraphs($term, "field_publication");
//      $publicationsList = [];
//      foreach ($publications as $publication) {
//        array_push($publicationsList, new Publication($publication));
//      }
//      return $publicationsList;

    }

	public static function termLoadPartnerByName($term_name) {
		// This is just for Partners cw 2018-05-14
      $clean_name = str_replace('-', ' ', strtolower($term_name));
      $term_matches = taxonomy_term_load_multiple_by_name($clean_name, "partners");
      $term = null;
      if (count($term_matches) > 0) {
        $term = array_pop($term_matches);
      }
      return $term;
    }

    public static function termLoadDataProvidersByName($term_name) {
		// Data Providers cw 2018-07-03
		$clean_name = str_replace('-', ' ', strtolower($term_name));var_dump($clean_name);
      $term_matches = taxonomy_term_load_multiple_by_name($clean_name, "data providers");
      $term = null;
      if (count($term_matches) > 0) {
        $term = array_pop($term_matches);
      }
      return $term;
    }


    public static function getBandType($current_node) {
      $band_type_term = NodeUtil::termLoad($current_node->field_band_type[0]->target_id);
      return $band_type_term->label();
    }
  }

