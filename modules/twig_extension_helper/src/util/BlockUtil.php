<?php
/**
 * Created by IntelliJ IDEA.
 * User: sdave
 * Date: 2/27/2018
 * Time: 1:12 PM
 */

namespace Drupal\twig_extension_helper\util;


class BlockUtil {
  public static function getConfigKey($config, $key) {
    if (!empty($config[$key])) {
      return $config[$key];
    } else {
      return null;
    }
  }
}
