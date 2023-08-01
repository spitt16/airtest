namespace Drupal\navigation_link\Plugin\Field\FieldType;

use Drupal\Core\Field\FieldItemBase;
use Drupal\Core\Field\FieldDefinitionInterface;
use Drupal\Core\Field\FieldStorageDefinitionInterface;
use Drupal\Core\TypedData\DataDefinition;

/**
* Provides a field type of navigation_link.
*
* @FieldType(
*   id = "navigation_link",
*   label = @Translation("Navigation Link field"),
*   default_formatter = "navigation_link_formatter",
*   default_widget = "navigation_link_widget",
* )
*/

class NavigationLinkItem extends FieldItemBase {
  public static function schema(FieldStorageDefinitionInterface $field_definition) {
    return array(
      'columns' => array(
        'value' => array(
          'type' => 'text',
          'size' => 'tiny',
          'not null' => FALSE,
        ),
      ),
    );
  }

  /**
  * {@inheritdoc}
  */
  public function isEmpty() {
    $value = $this->get('value')->getValue();
    return $value === NULL || $value === '';
  }

  /**
  * {@inheritdoc}
  */
  public static function propertyDefinitions(FieldStorageDefinitionInterface $field_definition) {
    $properties['value'] = DataDefinition::create('string')->setLabel(t('Hex value'));

    return $properties;
  }
}
