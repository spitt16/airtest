<?php /**
 * @file
 * Contains \Drupal\miniorange_saml\Controller\DefaultController.
 */

namespace Drupal\miniorange_saml\Controller;

use Drupal\user\Entity\User;
use Drupal\Core\Controller\ControllerBase;
use Drupal\user\RoleInterface;
use Drupal\user\UserInterface;
use Symfony\Component\HttpFoundation\RedirectResponse;
use Drupal\miniorange_saml\Utilities;
use Drupal\miniorange_saml\MiniOrangeAuthnRequest;
use Drupal\miniorange_saml\MiniOrangeAcs;
use Drupal\miniorange_saml\XMLSecurityKey;
use Drupal\Core\DependencyInjection;
use DOMElement;

/**
 * Default controller for the miniorange_saml module.
 */
class miniorange_samlController extends ControllerBase {

  public function saml_login() {
    global $base_url;
	$b_url = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_base_url');
	$base_site_url = isset($b_url)? $b_url : $base_url;
    $entityID = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_entity_id');
    $issuer = isset($entityID)? $entityID : $base_site_url;
    $relay_state = $base_url;
    $acs_url = $base_url . '/samlassertion';
    $sso_url = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_idp_login_url');
    $authn_request = new MiniOrangeAuthnRequest();
    $redirect = $authn_request->initiateLogin($acs_url, $sso_url, $issuer, $relay_state);
	$response = new RedirectResponse($redirect);
    $response->send();
  }

  public function saml_response() {
global $base_url;
	$b_url = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_base_url');
	$base_site_url = isset($b_url)? $b_url : $base_url;  
	$acs_url = $base_site_url . '/samlassertion';

    $cert_fingerprint = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_idp_x509_certificate');
    $issuer = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_idp_issuer');
    $sp_entity_id = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_sp_issuer');

    $login_by = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_login_by');

    if ($login_by == 1) {
      $username_attribute = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_username_attribute');
    }
    else {
      $username_attribute = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_email_attribute');
    }

    if (isset($_GET['SAMLResponse'])) {
      session_destroy();
      global $base_url;
	  $response = new RedirectResponse($base_site_url);
	  $response->send();
    }
      $response_obj = new MiniOrangeAcs();
      $response = $response_obj->processSamlResponse($_POST, $acs_url, $cert_fingerprint, $issuer, $base_site_url , $sp_entity_id, $username_attribute, $attrs, $role);
		
      if (\Drupal::config('miniorange_saml.settings')->get('miniorange_saml_login_by') == 1) {
        $account = user_load_by_name($response['username']);
      }
      else {
        $account = user_load_by_mail($response['username']);
      }
	  
      // Create user if not already present.
      if ($account == NULL) {
        $default_role = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_default_role');
        $disable_autocreate_users = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_disable_autocreate_users');
        if ($disable_autocreate_users) {
          echo 'Account does not exist with your username. Close this browser and try with different user.';
          exit();
        }
        else {
		
          $random_password = user_password(8);
          $new_user = [
            'name' => $response['username'],
            'mail' => $response['email'],
            'pass' => $random_password,
            'status' => 1,
          ];
          // user_save() is now a method of the user entity.
		   $account = User::create($new_user);
           $account -> save();

        }
      }

      $customFieldAttributes = $response['customFieldAttributes'];
      foreach ($customFieldAttributes as $key => $value) {
        $account = \Drupal::entityManager()->getStorage('user')->load($account->uid);
        $account->{$key}['und'][0]['value'] = $value;
        $account->save();
      }
	  
      if (user_is_blocked($response['username']) == FALSE) {
      if (!empty($s1) && isset($s1)) {
			$rediectUrl = $s1;
		}
		
		else if (array_key_exists('relay_state', $response) && !empty($response['relay_state'])) {
          $rediectUrl = $response['relay_state'];
		}
		
        $_SESSION['sessionIndex'] = $response['sessionIndex'];
        $_SESSION['NameID'] = $response['NameID'];
        $_SESSION['mo_saml']['logged_in_with_idp'] = TRUE;

        user_login_finalize($account);
		
        $response = new RedirectResponse($rediectUrl);
        $response->send();
		return;
      }
      else {
        echo("User Blocked By Administrator");
        exit;
      }
	 
    }

  function saml_logout() {
	  $base_url = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_base_url');
	  if(is_null($_REQUEST['RelayState'])) {
		  $_REQUEST['RelayState'] = $base_url;
	  }
    session_destroy();
	$response = new RedirectResponse($_REQUEST['RelayState']);
    $response->send();
    exit;
	return;
  }

/**
* Test configuration callback
*/  
  
  function test_configuration() {
	global $base_url;
	$b_url = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_base_url');
	$base_site_url = isset($b_url)? $b_url : $base_url;  

	$sendRelayState = "testValidate";
    $ssoUrl = \Drupal::config('miniorange_saml.settings')->get("miniorange_saml_idp_login_url");
    $acsUrl = $base_site_url . "/samlassertion";
    	$entityID = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_entity_id');
	$issuer = isset($entityID)? $entityID : $base_site_url;
	$samlRequest = Utilities::createAuthnRequest($acsUrl, $issuer, FALSE);
    $redirect = $ssoUrl;
    if (strpos($ssoUrl, '?') !== FALSE) {
      $redirect .= '&';
    }
    else {
      $redirect .= '?';
    }
    $redirect .= 'SAMLRequest=' . $samlRequest . '&RelayState=' . urlencode($sendRelayState);
	$response = new RedirectResponse($redirect);
    $response->send();
	return;
  }
}