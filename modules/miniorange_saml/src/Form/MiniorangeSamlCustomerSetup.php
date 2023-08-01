<?php

/**
 * @file
 * Contains \Drupal\miniorange_saml\Form\MiniorangeSamlCustomerSetup.
 */

namespace Drupal\miniorange_saml\Form;

use Drupal\miniorange_saml\MiniorangeSAMLCustomer;
use Drupal\miniorange_saml\AESEncryption;
use Drupal\Core\Form\FormBase;
use Drupal\Core\Form\FormStateInterface;
use Drupal\Core\Render\Element;
use Symfony\Component\HttpFoundation\RedirectResponse;
class MiniorangeSamlCustomerSetup extends FormBase {


  public function getFormId() {
    return 'miniorange_saml_customer_setup';
  }

  public function buildForm(array $form, \Drupal\Core\Form\FormStateInterface $form_state) {

    $current_status = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_status');

	if ($current_status == 'VALIDATE_OTP') {
        $form['miniorange_saml_customer_otp_token'] = array(
          '#type' => 'textfield',
          '#title' => t('OTP'),
        );

        $form['miniorange_saml_customer_validate_otp_button'] = array(
          '#type' => 'submit',
          '#value' => t('Validate OTP'),
          '#submit' => array('::miniorange_saml_validate_otp_submit'),
        );

        $form['miniorange_saml_customer_setup_resendotp'] = array(
          '#type' => 'submit',
          '#value' => t('Resend OTP'),
          '#submit' => array('::miniorange_saml_resend_otp'),
        );

        $form['miniorange_saml_customer_setup_back'] = array(
          '#type' => 'submit',
          '#value' => t('Back'),
          '#submit' => array('::miniorange_saml_back'),
        );

        return $form;
      }
      elseif ($current_status == 'PLUGIN_CONFIGURATION') {
       
        $form['markup_top'] = array(
          '#markup' => '<div>Thank you for registering with miniOrange</div>' . '<h4>Your Profile: </h4>'
          );

        $header = array(
          'email' => array('data' => t('Customer Email')),
          'customerid' => array(
            'data' => t('Customer ID')
            ),
          'token' => array('data' => t('Token Key')),
          'apikey' => array(
            'data' => t('API Key')
            ),
        );

        $options = [];

        $options[0] = array(
          'email' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_customer_admin_email'),
          'customerid' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_customer_id'),
          'token' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_customer_admin_token'),
          'apikey' => \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_customer_api_key'),
        );

        $form['fieldset']['customerinfo'] = array(
          '#theme' => 'table',
          '#header' => $header,
          '#rows' => $options,
        );

        return $form;
      }


    $form['markup_14'] = array('#markup' => '<h3>Register with miniOrange</h3>');

    $form['markup_15'] = array(
      '#markup' => 'Just complete the short registration below to configure' . ' the SAML Plugin. Please enter a valid email id <br>that you have' . ' access to. You will be able to move forward after verifying an OTP' . ' that we will send to this email.'
      );

    $form['miniorange_saml_customer_setup_username'] = array(
      '#type' => 'textfield',
      '#title' => t('Email'),
      '#required' => TRUE,
    );

    $form['miniorange_saml_customer_setup_phone'] = array(
      '#type' => 'textfield',
      '#title' => t('Phone'),
    );

    $form['markup_16'] = array(
      '#markup' => '<b>NOTE:</b> We will only call if you need support.'
      );

    $form['miniorange_saml_customer_setup_password'] = array(
      '#type' => 'password_confirm',
      '#required' => TRUE,
    );

    $form['miniorange_saml_customer_setup_button'] = array(
      '#type' => 'submit',
      '#value' => t('Register'),
    );
	
    return $form;

  }
    
  public function submitForm(array &$form, \Drupal\Core\Form\FormStateInterface $form_state) {
		
    $username = $form['miniorange_saml_customer_setup_username']['#value'];
    $phone = $form['miniorange_saml_customer_setup_phone']['#value'];
    $password = $form['miniorange_saml_customer_setup_password']['#value']['pass1'];

    $customer_config = new MiniorangeSAMLCustomer($username, $phone, $password, NULL);
    $check_customer_response = json_decode($customer_config->checkCustomer());
    if ($check_customer_response->status == 'CUSTOMER_NOT_FOUND') {
      // Create customer.
    // Store email and phone.
      \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_customer_admin_email', $username)->save();
      \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_customer_admin_phone', $phone)->save();
      \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_customer_admin_password', $password)->save();

      $send_otp_response = json_decode($customer_config->sendOtp());
	  
      if ($send_otp_response->status == 'SUCCESS') {
        \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_tx_id', $send_otp_response->txId)->save();
        $current_status = 'VALIDATE_OTP';
        \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_status', $current_status)->save();
        drupal_set_message(t('Verify email address by entering the passcode sent to @username', [
          '@username' => $username
          ]));
      }
    }
    elseif ($check_customer_response->status == 'CURL_ERROR') {
      drupal_set_message(t('cURL is not enabled. Please enable cURL'), 'error');
    }
    else {
      // Customer exists. Retrieve keys.
      $customer_keys_response = json_decode($customer_config->getCustomerKeys());

      if (json_last_error() == JSON_ERROR_NONE) {
        \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_customer_id', $customer_keys_response->id)->save();
        \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_customer_admin_token', $customer_keys_response->token)->save();
        \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_customer_admin_email', $username)->save();
        \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_customer_admin_phone', $phone)->save();
        \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_customer_api_key', $customer_keys_response->apiKey)->save();
        $current_status = 'PLUGIN_CONFIGURATION';
        \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_status', $current_status)->save();
        drupal_set_message(t('Successfully retrieved your account.'));

      }
      else {
        drupal_set_message(t('Invalid credentials'), 'error');
      }

      if (\Drupal::config('miniorange_saml.settings')->get('miniorange_saml_license_key')) {

        $key = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_customer_admin_token');
        $code = AESEncryption::decrypt_data(\Drupal::config('miniorange_saml.settings')->get('miniorange_saml_license_key'), $key);
        $username = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_customer_admin_email');
        $phone = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_customer_admin_phone');
        $customer = new MiniorangeSAMLCustomer($username, $phone, NULL, NULL);
        $content = json_decode($customer->verifyLicense($code), TRUE);

        if (strcasecmp($content['status'], 'SUCCESS') == 0) {

          drupal_set_message(t('Your license is verified. You can now setup the plugin.'));
        }
        else {
          drupal_set_message(t('License key for this instance is incorrect. Make sure you have not tampered with it at all. Please enter a valid license key.'), 'error');
          \Drupal::config('miniorange_saml.settings')->clear('miniorange_saml_license_key')->save();
        }
      }
      else {
        $current_status = 'PLUGIN_CONFIGURATION';
        \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_status', $current_status)->save();
      }
    }
  }

/**
 * Handle back button submit for customer setup.
 */
function miniorange_saml_back(&$form, $form_state) {
  $current_status = 'CUSTOMER_SETUP';
  \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_status', $current_status)->save();
  \Drupal::configFactory()->getEditable('miniorange_saml.settings')->clear('miniorange_miniorange_saml_customer_admin_email')->save();
  \Drupal::configFactory()->getEditable('miniorange_saml.settings')->clear('miniorange_saml_customer_admin_phone')->save();
  \Drupal::configFactory()->getEditable('miniorange_saml.settings')->clear('miniorange_saml_tx_id')->save();

  drupal_set_message(t('Register/Login with your miniOrange Account'),'status');
}  
  
/**
 * Resend OTP.
 */
public function miniorange_saml_resend_otp(&$form, $form_state) {

  \Drupal::configFactory()->getEditable('miniorange_saml.settings')->clear('miniorange_saml_tx_id')->save();
  $username = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_customer_admin_email');
  $phone = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_customer_admin_phone');
  $customer_config = new MiniorangeSAMLCustomer($username, $phone, NULL, NULL);
  $send_otp_response = json_decode($customer_config->sendOtp());
  if ($send_otp_response->status == 'SUCCESS') {
    // Store txID.
	\Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_tx_id', $send_otp_response->txID)->save();
    $current_status = 'VALIDATE_OTP';
	\Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_status', $current_status)->save();
    drupal_set_message(t('Verify email address by entering the passcode sent to @username', array('@username' => $username)));
  }
}

  
/**
 * Validate OTP.
 */
public function miniorange_saml_validate_otp_submit(&$form, $form_state) {

  $otp_token = $form['miniorange_saml_customer_otp_token']['#value'];
  $username = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_customer_admin_email');
  $phone = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_customer_admin_phone');
  $tx_id = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_tx_id');
  $customer_config = new MiniorangeSAMLCustomer($username, $phone, NULL, $otp_token);
  $validate_otp_response = json_decode($customer_config->validateOtp($tx_id));

  if ($validate_otp_response->status == 'SUCCESS') {
    // OTP Validated. Show Configuration page.
    $current_status = 'PLUGIN_CONFIGURATION';
    \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_status', $current_status)->save();
    \Drupal::configFactory()->getEditable('miniorange_saml.settings')->clear('miniorange_saml_tx_id')->save();

    // OTP Validated. Create customer.
    $password = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_customer_admin_password');
    $customer_config = new MiniorangeSAMLCustomer($username, $phone, $password, NULL);
    $create_customer_response = json_decode($customer_config->createCustomer());
    if ($create_customer_response->status == 'SUCCESS') {
      // Customer created.
       $current_status = 'PLUGIN_CONFIGURATION';
      \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_status', $current_status)->save();
      \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_customer_admin_email', $username)->save();
      \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_customer_admin_phone', $phone)->save();
      \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_customer_admin_token', $create_customer_response->token)->save();
      \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_customer_id', $create_customer_response->id)->save();
      \Drupal::configFactory()->getEditable('miniorange_saml.settings')->set('miniorange_saml_customer_api_key', $create_customer_response->apiKey)->save();

      drupal_set_message(t('Customer account created. Please verify your license key to activate plugin'));
	  $response = new RedirectResponse('admin/config/people/miniorange_saml/licensing');
	  $response->send();
    }
    else {
      drupal_set_message(t('Error creating customer'), 'error');
    }
  }
  else {
    drupal_set_message(t('Error validating OTP'), 'error');
  }
}

}