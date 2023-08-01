<?php
namespace Drupal\twig_extension_helper\util;


class ModelUtil {
  public static function stringToCleanKey($str) {
    $clean_str = str_replace(' ', '_', strtolower($str));
    return $clean_str;
  }

  public static function keyToLinkTarget($str_key) {
    if($str_key == "current_tab") {
      return "_self";
    }
    return "_blank";
  }

  public static function isFirstNull($obj) {
    return is_null($obj[0]);
  }

  public static function stringToCleanPath($str) {
    $clean_str = str_replace(' ', '-', strtolower($str));
    return $clean_str;
  }

  public static function getBooleanValue($obj, $field_name) {
    return self::helpGetField($obj, $field_name, "boolval");
  }

  public static function getValue($obj, $field_name) {
    return self::helpGetValue($obj, $field_name, NULL);
  }

  public static function getTrimmedValue($obj, $field_name) {
    return self::helpGetValue($obj, $field_name, "trim");
  }

  public static function getCleanKeyValue($obj, $field_name) {
    return self::helpGetValue($obj, $field_name, 'self::stringToCleanPath');
  }

  private static function helpGetValue($obj, $field_name, $type_callback=NULL) {
    if($obj->hasField($field_name)) {
      $fields = $obj->get($field_name);
      if(count($fields) == 1) {
        if(is_null($type_callback)) {
          return self::helpGetField($fields[0]);
        } else {
          return call_user_func($type_callback, self::helpGetField($fields[0]));
        }
      } else if(count($fields) > 0) {
        $field_arr = [];

        foreach($fields as $field) {
          if(is_null($type_callback)) {
            array_push($field_arr, self::helpGetField($field));
          } else {
            array_push($field_arr, call_user_func($type_callback, self::helpGetField($field)));
          }
        }

        return $field_arr;
      }
    }
    return NULL;
  }


  private static function helpGetField($field_obj) {
    if(!is_null($field_obj->value)) {
      if (!is_null($field_obj->format)) {
        return check_markup($field_obj->value, $field_obj->format);
      }
      return $field_obj->value;
    } else if (!is_null($field_obj->target_id)) {
      return $field_obj->target_id;
    }
    return NULL;
  }
}

