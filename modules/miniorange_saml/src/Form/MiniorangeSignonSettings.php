<?php
/**
 * @file
 * Contains Login Settings for miniOrange SAML Login Module.
 */

 /**
 * Showing Settings form.
 */
 namespace Drupal\miniorange_saml\Form;
 
 use Drupal\Core\Form\FormBase;
 
 class MiniorangeSignonSettings extends FormBase {
	 
  public function getFormId() {
    return 'miniorange_saml_login_setting';
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

  $form['markup_1'] = array(
    '#markup' => '<h2>Sign in Settings</h2>',
  );

  $form['miniorange_saml_force_auth'] = array(
    '#type' => 'checkbox',
    '#title' => t('Protect website against anonymous access <b>[PREMIUM]</b>'),
    '#default_value' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_force_auth'),
    '#disabled' => TRUE,
  );

  $form['markup_2'] = array(
    '#markup' => '<b>Note: </b>Users will be redirected to your IdP for login in case user is not logged in and tries to access website.<br><br>',
  );

$form['miniorange_saml_auto_redirect'] = array(
    '#type' => 'checkbox',
    '#title' => t('Check this option if you want to <b>auto redirect the user to IdP [PREMIUM]</b>'),
    '#default_value' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_auto_redirect_to_idp'),
	'#disabled' => TRUE,
  );

  $form['markup_3'] = array(
    '#markup' => 'Note: Users will be redirected to your IdP for login when the login page is accessed.<br><br>',
  );

  $form['miniorange_saml_enable_backdoor'] = array(
    '#type' => 'checkbox',
    '#title' => t('Check this option if you want to enable <b>backdoor login [PREMIUM]</b>'),
    '#default_value' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_enable_backdoor'),
    '#disabled' => TRUE,
  );

  $form['markup_4'] = array(
    '#markup' => '<b>Note: </b>Checking this option <b>creates a backdoor to login to your Website using Drupal credentials</b><br>' 
    . ' incase you get locked out of your IdP. Note down this URL: <b>' . $base_url . '/saml_login=false</b><br><br>',
  );
  
  $form['miniorange_saml_default_relaystate'] = array(
    '#type' => 'textfield',
    '#title' => t('Default Redirect URL after login <b>[PREMIUM]</b>'),
    '#default_value' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_default_relaystate'),
    '#attributes' => array('placeholder' => 'Enter Default Redirect URL'),
	'#disabled' => TRUE,
  );
    
  $form['miniorange_saml_gateway_config_submit'] = array(
    '#type' => 'submit',
    '#value' => t('Save Configuration'),
  );
  
  return $form;

 }

  public function submitForm(array &$form, \Drupal\Core\Form\FormStateInterface $form_state) {

  $auto_redirect = $form['miniorange_saml_auto_redirect']['#value'];
  $force_authentication = $form['miniorange_saml_force_auth']['#value'];
  $enable_backdoor = $form['miniorange_saml_enable_backdoor']['#value'];
  
  if ($auto_redirect == 1) {
    $auto_redirect = TRUE;
  }
  else {
    $auto_redirect = FALSE;
  }
  
  if ($force_authentication == 1) {
    $force_authentication = TRUE;
  }
  else {
    $force_authentication = FALSE;
  }

  if ($enable_backdoor == 1) {
    $enable_backdoor = TRUE;
  }
  else {
    $enable_backdoor = FALSE;
  }
  
  \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_auto_redirect_to_idp', $auto_redirect)->save();
  \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_force_auth', $force_authentication)->save();
  \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_enable_backdoor', $enable_backdoor)->save();
  
  drupal_set_message(t('Signin Settings successfully saved'));

 }
 }