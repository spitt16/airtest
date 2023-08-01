<?php
/**
 * Created by IntelliJ IDEA.
 * User: sdave
 * Date: 2/28/2018
 * Time: 10:01 AM
 */

namespace Drupal\twig_extension_helper\model;


use Drupal\twig_extension_helper\CurrentAQBandMapIcon;
use Drupal\twig_extension_helper\util\ParagraphUtil;

class CurrentAQBand extends Band {

  var $map_icons = [], $chart_filter_descriptions;

  function __construct($node_obj) {
    parent::__construct($node_obj);

    $li_map_icons = ParagraphUtil::getParagraphs($node_obj, "field_current_band_map_icons");
    foreach($li_map_icons as $li_map_icon) {
      array_push($this->map_icons, new CurrentAQBandMapIcon($li_map_icon));
    }

    $paragraphs_chart_descs = ParagraphUtil::getParagraph($node_obj, "field_hc_chart_filter_descs");
    if(!is_null($paragraphs_chart_descs)) {
      $this->chart_filter_descriptions = new ChartFilterDescriptions($paragraphs_chart_descs);
    }
  }

  /**
   * @return array
   */
  public function getMapIcons() {
    return $this->map_icons;
  }

  public function hasMapIcons() {
    if(count($this->map_icons) > 0) {
      return true;
    }
    return false;
  }

  /**
   * @return \Drupal\twig_extension_helper\model\ChartFilterDescriptions
   */
  public function getChartFilterDescriptions() {
    return $this->chart_filter_descriptions;
  }

  public function hasChartFilterDescriptions() {
    return !is_null($this->chart_filter_descriptions);
  }


}
