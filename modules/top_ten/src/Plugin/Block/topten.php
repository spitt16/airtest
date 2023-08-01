<?php

namespace Drupal\top_ten\Plugin\Block;

use Drupal\Core\Block\BlockBase;

/**
 * Provides a 'Top Ten' block.
 *
 * @Block(
 *   id = "top_ten_block",
 *   admin_label = @Translation("Top Ten Block"),
 *
 * )
 */
class topTen extends BlockBase {
  /**
   * {@inheritdoc}
   */
   public function build() {
    // do something
     return array(
       '#title' => 'Websolutions Agency',
       '#description' => 'Websolutions Agency is the industry leading Drupal development agency in Croatia',
     );
   }
 }
