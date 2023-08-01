<?php

/**
 * @file
 * Contains \Drupal\miniorange_saml\Form\MiniorangeIDPSetup.
 */

namespace Drupal\miniorange_saml\Form;

use Drupal\Core\Form\FormBase;
use Drupal\Core\Form\FormStateInterface;
use Drupal\Core\Render\Element;

class MiniorangeIDPSetup extends FormBase {

  public function getFormId() {
    return 'miniorange_saml_idp_setup';
  }

  public function buildForm(array $form, \Drupal\Core\Form\FormStateInterface $form_state) {

   
  if (\Drupal::config('miniorange_saml.settings')->get('miniorange_saml_customer_admin_email') == NULL || \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_customer_id') == NULL
    || \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_customer_admin_token') == NULL || \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_customer_api_key') == NULL) {
    $form['header'] = array(
      '#markup' => '<center><h3>You need to register with miniOrange before using this module.</h3></center>',
    );

    return $form;
  }
  
  global $base_url;
  $url = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_base_url');
  $issuer = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_entity_id');
  
  $b_url = isset($url) && !empty($url)? $url:$base_url;
  $issuer_id = isset($issuer) && !empty($issuer)? $issuer:$base_url;
  
  
  $acs_url = $b_url . '/samlassertion';
  $logout_url = $b_url . '/user/logout';
  
  
  $form['miniorange_saml_base_url'] = array(
    '#type' => 'textfield',
    '#title' => t('SP Base URL:'),
    '#default_value' => $b_url,
    '#attributes' => array(
		),
  );
  
  $form['miniorange_saml_entity_id'] = array(
    '#type' => 'textfield',
    '#title' => t('SP Entity ID/Issuer:'),
    '#default_value' => $issuer_id,
    '#attributes' => array(
		),
  );
  
  $form['miniorange_saml_idp_config_submit'] = array(
    '#type' => 'submit',
    '#value' => t('Save'),
  );
  
  $form['header'] = array(
    '#markup' => '<center><h3>You will need the following information to'
    . ' configure your IdP. Copy it and keep it handy</h3></center>',
  );

  $header = array(
    'attribute' => array('data' => t('Attribute')),
    'value' => array('data' => t('Value')),
  );

  $options = array();

  $options[0] = array(
    'attribute' => t('Issuer'),
    'value' => $issuer_id,
  );

  $options[1] = array(
    'attribute' => t('ACS URL'),
    'value' => $acs_url,
  );

  $options[2] = array(
    'attribute' => t('Audience URI'),
    'value' => $b_url,
  );

  $options[3] = array(
    'attribute' => t('Recipient URL'),
    'value' => $acs_url,
  );

  $options[4] = array(
    'attribute' => t('Destination URL'),
    'value' => $acs_url,
  );

  $options[5] = array(
    'attribute' => t('Single Logout URL'),
    'value' => $logout_url,
  );
  
  $options[6] = array(
    'attribute' => t('NameID Format'),
    'value' => 'urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress',
  );

  $form['fieldset']['spinfo'] = array(
    '#theme' => 'table',
    '#header' => $header,
    '#rows' => $options,
  );
  
  $form['markup_sp_md_1'] = array(
    '#markup' => 'You can provide this metadata URL to your Identity Provider.<br />',
  );

  $form['markupsp_sp_md_2'] = array(
    '#markup' => '<code style="background-color:gainsboro;"><b>'
	. '<a target="_blank" href="' . $b_url . '/modules/miniorange_saml/includes/metadata/metadata.php">' . $b_url . '/modules/miniorange_saml/includes/metadata/metadata.php' . '</a></b></code>',
  );

  $form['markup_13'] = array(
    '#markup' => '<h3>Identity Provider Guides</h3>',
  );

  $form['markup_14'] = array(
    '#markup' => 'With the help of the above information, you can configure your IdP. We also have guides for configuring various IdP\'s<br>'
    . '<a href="' . $b_url . '/' . drupal_get_path('module', 'miniorange_saml') . '/idp_guides/miniorange_as_idp.pdf" target="_blank">Click here to see the Guide for Configuring miniOrange as IdP. </a><br>',
  );

  $form['markup_15'] = array(
    '#markup' => '<a href="' . $b_url . '/' . drupal_get_path('module', 'miniorange_saml') . '/idp_guides/okta_as_idp.pdf" target="_blank">Click here to see the Guide for Configuring Okta '
    . 'as IdP. </a><br>',
  );

  $form['markup_16'] = array(
    '#markup' => '<b>NOTE: </b> We also have step by step do-it-yourself guides available for all known IdPs like ADFS, Centrify, Okta, '
    . 'OneLogin, OpenAM, Oracle Identity Manager, JBoss Keycloak, Salesforce, Shibboleth, SimpleSAML, WSO2 etc. '
  );

  return $form;

  }
  
  public function submitForm(array &$form, \Drupal\Core\Form\FormStateInterface $form_state) {
	$b_url = $form['miniorange_saml_base_url']['#value'];
	$issuer_id = $form['miniorange_saml_entity_id'] ['#value'];
	
	 \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_base_url', $b_url)->save();
	 \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_entity_id', $issuer_id)->save();
	 
  }
    
}