<?php
/**
 * Created by IntelliJ IDEA.
 * User: sdave
 * Date: 1/16/2018
 * Time: 11:10 AM
 */

namespace Drupal\twig_extension_helper\model;


class ParameterMessage {

  var $category_key,
//    $category_string, TODO: Add ability to get label of category key
    $message,
    $forecastMessage;

  function __construct($paragraph_obj) {
    $this->setCategoryKey($paragraph_obj->field_parameter_category[0]->value);
//    $this->setCategoryString(?);
    $this->setMessage($paragraph_obj->field_parameter_description_obse[0]->value);
    $this->setForecastMessage($paragraph_obj->field_parameter_description_fore[0]->value);

  }

  /**
   * @return mixed
   */
  public function getCategoryKey() {
    return $this->category_key;
  }

  /**
   * @param mixed $category_key
   */
  protected function setCategoryKey($category_key) {
    $this->category_key = $category_key;
//    $this->category_key = ModelUtil::stringToCleanKey($category_key);
  }

  /**
   * @return mixed
   */
  public function getMessage() {
    return $this->message;
  }

  /**
   * @param mixed $message
   */
  protected function setMessage($message) {
    $this->message = $message;
  }

  /**
   * @return mixed
   */
  public function getForecastMessage() {
    return $this->forecastMessage;
  }

  /**
   * @param mixed $message
   */
  protected function setForecastMessage($forecastMessage) {
    $this->forecastMessage = $forecastMessage;
  }

//  /**
//   * @return mixed
//   */
//  public function getCategoryString() {
//    return $this->category_string;
//  }
//
//  /**
//   * @param mixed $category_string
//   */
//  protected function setCategoryString($category_string) {
//    $this->category_string = $category_string;
//  }



}
