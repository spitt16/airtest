<?php
/**
 * Created by IntelliJ IDEA.
 * User: sdave
 * Date: 3/16/2018
 * Time: 3:08 PM
 */

namespace Drupal\twig_extension_helper\model;


use Drupal\twig_extension_helper\util\ModelUtil;

class ChartFilterDescriptions {

  var $day_description, $week_description, $month_description;

  function __construct($filter_descriptions_obj) {
    $this->day_description = ModelUtil::getValue($filter_descriptions_obj, "field_hc_chart_filter_day_desc");
    $this->week_description = ModelUtil::getValue($filter_descriptions_obj, "field_hc_chart_filter_month_desc");
    $this->month_description = ModelUtil::getValue($filter_descriptions_obj, "field_hc_chart_filter_week_desc");
  }

  /**
   * @return array|null
   */
  public function getDayDescription() {
    return $this->day_description;
  }

  /**
   * @return array|null
   */
  public function getWeekDescription() {
    return $this->week_description;
  }

  /**
   * @return array|null
   */
  public function getMonthDescription() {
    return $this->month_description;
  }


}
