<?php
/**
 * @file
 * Contains Licensing information for miniOrange SAML Login Module.
 */

 /**
 * Showing Licensing form info.
 */
namespace Drupal\miniorange_saml\Form;

use Drupal\Core\Form\FormBase;
use Drupal\Core\Form\FormStateInterface;
 

class MiniorangeLicensing extends FormBase {
	
public function getFormId() {
    return 'miniorange_saml_licensing';
  }
 
public function buildForm(array $form, \Drupal\Core\Form\FormStateInterface $form_state) {

  $dyi_plan = "'drupal_miniorange_saml_basic_plan'";
  $premium_plan = "'drupal_miniorange_saml_premium_plan'";
  $more_instances_plan = "'drupal_miniorange_saml_upgrade_instances_plan'";
  $admin_username = "'" . \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_customer_admin_email') . "'";

  if(\Drupal::config('miniorange_saml.settings')->get('miniorange_saml_license_key') == NULL){
    $form['markup_1'] = array(
      '#markup' => '<div class="mo_saml_table_layout">'
      . '<table class="mo_saml_local_pricing_table">'
      . '<h2>Licensing Plans</h2><hr>'
      . '<tr style="vertical-align:top;">',
    );

    $form['markup_2'] = array(
      '#markup' => '<td><div class="mo_saml_local_thumbnail mo_saml_local_pricing_paid_tab" >'
      . '<h3 class="mo_saml_local_pricing_header">Do it yourself</h3><p></p>'
      . '<h4 class="mo_saml_local_pricing_sub_header" style="padding-bottom:8px !important;">'
      . '<a class="btn btn-primary btn-large" style="padding:5px;" onclick="payment(' . $dyi_plan .', ' 
      . $admin_username .');">Click to Upgrade</a>*</h4><hr>'
      . '<p class="mo_saml_local_pricing_text" style="padding:10px;">$349 - One Time Payment</p><br><hr>'
      . '<p class="mo_saml_local_pricing_text">'
      . 'Unlimited Authentications via IdP<br>Customized Role Mapping<br>Customized Attribute Mapping<br>'
      . 'Auto-Redirect to IdP<br>Step-By-Step Guide to Setup IdP<br>Single Logout<br>Protect your whole site<br>'
      . 'Options to select SAML Request Binding Type<br>Integrated Windows Authentication<br><br><br/></p><hr>'
      . '<p class="mo_saml_local_pricing_text" >Basic Support by Email</p></div></td>',
    );
  } else{
    $form['markup_1'] = array(
      '#markup' => '<div class="mo_saml_table_layout">'
      . '<table class="mo_saml_local_pricing_table">'
      . '<h2>Licensing Plans</h2><hr>'
      . '<tr style="vertical-align:top;">',
    );

    $form['markup_2'] = array(
      '#markup' => '<td><div class="mo_saml_local_thumbnail mo_saml_local_pricing_paid_tab" >'
      . '<h3 class="mo_saml_local_pricing_header">Do it yourself</h3><p></p>'
      . '<h4 class="mo_saml_local_pricing_sub_header" style="padding-bottom:8px !important;">'
      . '<a class="btn btn-primary btn-large" style="padding:5px;" onclick="payment(' . $more_instances_plan .', ' 
      . $admin_username .');">Buy More Instances</a>*</h4><hr>'
      . '<p class="mo_saml_local_pricing_text" style="padding:10px;">$349 - One Time Payment</p><hr>'
      . '<p class="mo_saml_local_pricing_text">'
      . 'Unlimited Authentications via IdP<br>Customized Role Mapping<br>Customized Attribute Mapping<br>'
      . 'Auto-Redirect to IdP<br>Step-By-Step Guide to Setup IdP<br>Single Logout<br>Protect your whole site<br>'
      . 'Options to select SAML Request Binding Type<br>Integrated Windows Authentication<br><br><br/></p><hr>'
      . '<p class="mo_saml_local_pricing_text" >Basic Support by Email</p></div></td>',
    );
  }

  $form['markup_3'] = array(
    '#markup' => '<td><div class="mo_saml_local_thumbnail mo_saml_local_pricing_free_tab" >'
    . '<h3 class="mo_saml_local_pricing_header">Premium</h3><p></p>'
    . '<h4 class="mo_saml_local_pricing_sub_header" style="padding-bottom:8px !important;">'
    . '<a class="btn btn-primary btn-large" style="padding:5px;" onclick="payment(' . $premium_plan .', ' 
    . $admin_username .');">Click to upgrade</a>*</h4><hr>'
    . '<p class="mo_saml_local_pricing_text">$349 + One Time Setup Fees <br>( $60 per hour )</p><hr>'
    . '<p class="mo_saml_local_pricing_text">Unlimited Authentications via IdP<br>Customized Role Mapping<br>'
    . 'Customized Attribute Mapping<br>Auto-Redirect to IdP<br>Step-By-Step Guide to Setup IdP<br>Single Logout<br>Protect your whole site<br>'
    . 'Options to select SAML Request Binding Type<br>Integrated Windows Authentication<br>Multiple IdP Support for Cloud Service Providers<br>'
    . 'End to End Identity Provider Configuration **<br></p><hr><p class="mo_saml_local_pricing_text">Premium Support Plans Available</p>'
    . '</div></td></tr></table>'
  );

  
  $form['markup_4'] = array(
    '#markup' => '<h3>Identity Providers Supported</h3>'
    . 'Google Apps, ADFS, Okta, Salesforce, Shibboleth, SimpleSAMLphp, OpenAM, Centrify, Ping, RSA'
    . ', IBM, Oracle, OneLogin, Bitium, WSO2, NetIQ, miniOrange Identity Provider'
  );

  $form['markup_5'] = array(
    '#markup' => '<h3>Steps to Upgrade to Premium Plugin</h3>'
    . '<ol><li>You will be redirected to miniOrange Login Console. Enter your password with which you created an'
    . ' account with us. After that you will be redirected to payment page.</li>'
    . '<li>Enter you card details and complete the payment. On successful payment completion, you will see the '
    . 'link to download the premium plugin.</li>'
    . 'Once you download the premium plugin, just unzip it and replace the folder with existing plugin. Clear Drupal Cache.</li></ol>'
  );

  $form['markup_6'] = array(
    '#markup' => '<h3>** End to End Identity Provider Integration</h3>'
    . 'We will setup a Conference Call / Gotomeeting and do end to end configuration for you for IDP '
    . 'as well as plugin. We provide services to do the configuration on your behalf.'
  );

  $form['markup_7'] = array(
    '#markup' => '<h3>*Integrated Windows Authentication</h3>'
    . 'With Integrated windows authentication, if the user comes to your Drupal Site from a domain joined machine'
    . ' then he will not even have to re-enter his credentials because he already did that when he unlocked his computer.</div>'
  );

  return $form;
 }
 
  public function submitForm(array &$form, \Drupal\Core\Form\FormStateInterface $form_state) {
  }
 }