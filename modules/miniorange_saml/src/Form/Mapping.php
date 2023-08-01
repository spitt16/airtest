<?php
/**
 * @file
 * Contains Attribute and Role Mapping for miniOrange SAML Login Module.
 */

 /**
 * Showing Settings form.
 */
namespace Drupal\miniorange_saml\Form;

use Drupal\Core\Form\FormBase;
use Drupal\Core\Form\FormStateInterface;

 class Mapping extends FormBase {
	 
  public function getFormId() {
    return 'miniorange_saml_mapping';
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
 
  // @FIXME
// Could not extract the default value because it is either indeterminate, or
// not scalar. You'll need to provide a default value in
// config/install/miniorange_saml.settings.yml and config/schema/miniorange_saml.schema.yml.
$form['miniorange_saml_account_username_by'] = array(
    '#type' => 'select',
    '#title' => t('Login/Create Drupal account by'),
    '#options' => array(
      1 => t('Username'),
      2 => t('Email'),
    ),
    '#default_value' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_login_by'),
  );

  $form['miniorange_saml_username_attribute'] = array(
    '#type' => 'textfield',
    '#title' => t('Username Attribute'),
    '#default_value' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_username_attribute'),
    '#attributes' => array('placeholder' => 'Enter Username attribute'),
    '#required' => TRUE,
  );

  $form['miniorange_saml_email_attribute'] = array(
    '#type' => 'textfield',
    '#title' => t('Email Attribute'),
    '#default_value' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_email_attribute'),
    '#attributes' => array('placeholder' => 'Enter Email attribute'),
    '#required' => TRUE,
  );
  
$form['miniorange_saml_idp_attr1_name'] = array(
	'#type' => 'textfield',
	'#title' => t('Role <b>[PREMIUM]</b>'),
	'#default_value' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_idp_attr1_name'),
	'#attributes' => array('placeholder' => 'Enter Role Attribute'),
	'#required' => FALSE,
	'#disabled' => TRUE,
  );
  
 
  $form['markup_cam'] = array(
    '#markup' => '<h3>Custom Attribute Mapping <b>[PREMIUM]</b></h3><p>Add the Drupal field attributes in the Attribute Name textfield and add the IdP attibutes that you need to map with the drupal attributes in the IdP Attribute Name textfield. Drupal Field Attributes will be of type text. Add the machine name of the attribute in the Drupal Attribute textfield.</p><p>For example: If the attribute name in the drupal is name then its machine name will be field_name.</p>',
  );
  
   $form['miniorange_saml_attr5_name'] = array(
	'#type' => 'textfield',
	'#title' => t('Attribute Name 1'),
	'#default_value' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_attr5_name'),
	'#attributes' => array('placeholder' => 'Enter Attribute Name'),
	'#required' => FALSE,
	'#disabled' => TRUE,
  );
  
  $form['miniorange_saml_idp_attr5_name'] = array(
	'#type' => 'textfield',
	'#title' => t('IdP Attribute Name 1'),
	'#default_value' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_idp_attr5_name'),
	'#attributes' => array('placeholder' => 'Enter IdP Attribute Name'),
	'#required' => FALSE,
	'#disabled' => TRUE,
  );
  
  $form['miniorange_saml_attr2_name'] = array(
	'#type' => 'textfield',
	'#title' => t('Attribute Name 2'),
	'#default_value' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_attr2_name'),
	'#attributes' => array('placeholder' => 'Enter Attribute Name'),
	'#required' => FALSE,
	'#disabled' => TRUE,
  );
  
  $form['miniorange_saml_idp_attr2_name'] = array(
	'#type' => 'textfield',
	'#title' => t('IdP Attribute Name 2'),
	'#default_value' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_idp_attr2_name'),
	'#attributes' => array('placeholder' => 'Enter IdP Attribute Name'),
	'#required' => FALSE,
	'#disabled' => TRUE,
  );
  
  $form['miniorange_saml_attr3_name'] = array(
	'#type' => 'textfield',
	'#title' => t('Attribute Name 3'),
	'#default_value' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_attr3_name'),
	'#attributes' => array('placeholder' => 'Enter Attribute Name'),
	'#required' => FALSE,
	'#disabled' => TRUE,
  );
  
  $form['miniorange_saml_idp_attr3_name'] = array(
	'#type' => 'textfield',
	'#title' => t('IdP Attribute Name 3'),
	'#default_value' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_idp_attr3_name'),
	'#attributes' => array('placeholder' => 'Enter IdP Attribute Name'),
	'#required' => FALSE,
	'#disabled' => TRUE,
  );
  
  $form['miniorange_saml_attr4_name'] = array(
	'#type' => 'textfield',
	'#title' => t('Attribute Name 4'),
	'#default_value' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_attr4_name'),
	'#attributes' => array('placeholder' => 'Enter Attribute Name'),
	'#required' => FALSE,
	'#disabled' => TRUE,
  );
  
  $form['miniorange_saml_idp_attr4_name'] = array(
	'#type' => 'textfield',
	'#title' => t('IdP Attribute Name 4'),
	'#default_value' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_idp_attr4_name'),
	'#attributes' => array('placeholder' => 'Enter IdP Attribute Name'),
	'#required' => FALSE,
	'#disabled' => TRUE,
  );
  
   $form['markup_role'] = array(
    '#markup' => '<h3>Custom Role Mapping <b>[PREMIUM]</b></h3>',
  );
  

$form['miniorange_saml_enable_rolemapping'] = array(
    '#type' => 'checkbox',
    '#title' => t('Check this option if you want to <b>enable Role Mapping</b>'),
    '#default_value' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_enable_rolemapping'),
	'#disabled' => TRUE,
  );
  
   $form['miniorange_saml_disable_autocreate_users'] = array(
    '#type' => 'checkbox',
    '#title' => t('Check this option if you want to disable <b>auto creation</b> of users if user does not exist.'),
    '#default_value' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_disable_autocreate_users'),
	'#disabled' => TRUE,
  );
  
	$mrole= user_roles($membersonly = TRUE);
    $form['miniorange_saml_default_mapping'] = array(
    '#type' => 'select',
	'#title' => t('Select default group for the new users'),
	'#options' => array_keys($mrole),
	'#default_value' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_default_role'),
	'#disabled' => TRUE,
   );
    
   $form['miniorange_saml_role1_name'] = array(
	'#type' => 'textfield',
	'#title' => t('Role Name 1'),
	'#default_value' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_role1_name'),
	'#attributes' => array('placeholder' => 'Enter Role Name'),
	'#required' => FALSE,
	'#disabled' => TRUE,
  );
  
  $form['miniorange_saml_idp_role1_name'] = array(
	'#type' => 'textfield',
	'#title' => t('IdP Role Name 1'),
	'#default_value' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_idp_role1_name'),
	'#attributes' => array('placeholder' => 'Enter IdP Role Name'),
	'#required' => FALSE,
	'#disabled' => TRUE,
  );
  
   $form['miniorange_saml_role2_name'] = array(
	'#type' => 'textfield',
	'#title' => t('Role Name 2'),
	'#default_value' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_role2_name'),
	'#attributes' => array('placeholder' => 'Enter Role Name'),
	'#required' => FALSE,
	'#disabled' => TRUE,
  );
  
  $form['miniorange_saml_idp_role2_name'] = array(
	'#type' => 'textfield',
	'#title' => t('IdP Role Name 2'),
	'#default_value' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_idp_role2_name'),
	'#attributes' => array('placeholder' => 'Enter IdP Role Name'),
	'#required' => FALSE,
	'#disabled' => TRUE,
  );
  
   $form['miniorange_saml_role3_name'] = array(
	'#type' => 'textfield',
	'#title' => t('Role Name 3'),
	'#default_value' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_role3_name'),
	'#attributes' => array('placeholder' => 'Enter Role Name'),
	'#required' => FALSE,
	'#disabled' => TRUE,
  );
  
  $form['miniorange_saml_idp_role3_name'] = array(
	'#type' => 'textfield',
	'#title' => t('IdP Role Name 3'),
	'#default_value' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_idp_role3_name'),
	'#attributes' => array('placeholder' => 'Enter IdP Role Name'),
	'#required' => FALSE,
	'#disabled' => TRUE,
  );
  
   $form['miniorange_saml_role4_name'] = array(
	'#type' => 'textfield',
	'#title' => t('Role Name 4'),
	'#default_value' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_role4_name'),
	'#attributes' => array('placeholder' => 'Enter Role Name'),
	'#required' => FALSE,
	'#disabled' => TRUE,
  );
  
  $form['miniorange_saml_idp_role4_name'] = array(
	'#type' => 'textfield',
	'#title' => t('IdP Role Name 4'),
	'#default_value' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_idp_role4_name'),
	'#attributes' => array('placeholder' => 'Enter IdP Role Name'),
	'#required' => FALSE,
	'#disabled' => TRUE,
  );
  
  $form['miniorange_saml_gateway_config_submit'] = array(
    '#type' => 'submit',
    '#value' => t('Save Configuration'),
  );
  return $form;

 }
 
  public function submitForm(array &$form, \Drupal\Core\Form\FormStateInterface $form_state) {
  
  $login_by = $form['miniorange_saml_account_username_by']['#value'];
  $username_attribute = $form['miniorange_saml_username_attribute']['#value'];
  $email_attribute = $form['miniorange_saml_email_attribute']['#value'];
 
  \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_login_by', $login_by)->save();
  \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_username_attribute', $username_attribute)->save();
  \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_email_attribute', $email_attribute)->save();
  \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_disable_autocreate_users', $enable_autocreate_users)->save();
  
  drupal_set_message(t('Signin Settings successfully saved'));
  }
  }