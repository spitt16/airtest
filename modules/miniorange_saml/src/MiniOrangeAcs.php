<?php
namespace Drupal\miniorange_saml;

use DOMDocument;
use DOMElement;
use Exception;
use Drupal\miniorange_saml\XMLSecurityKey;
use Drupal\miniorange_saml\SAML2_Response;

/**
 * The MiniOrangeAcs class.
 */
class MiniOrangeAcs {

  /**
   * The function processSamlResponse.
   */
  public function processSamlResponse($post, $acs_url, $cert_fingerprint, $issuer, $base_url, $spEntityId, $username_attribute, $custom_attributes, $custom_roles) {

    if (array_key_exists('SAMLResponse', $post)) {
		$saml_response = $post['SAMLResponse'];
    }
    else {
      throw new Exception('Missing SAMLRequest or SAMLResponse parameter.');
    }
    $saml_response = base64_decode($saml_response);
    $document = new DOMDocument();
    $document->loadXML($saml_response);

    $saml_response_xml = $document->firstChild;
	
    $cert_fingerprint = XMLSecurityKey::getRawThumbprint($cert_fingerprint);

    $saml_response = new SAML2_Response($saml_response_xml);
    $cert_fingerprint = preg_replace('/\s+/', '', $cert_fingerprint);
    $cert_fingerprint = iconv("UTF-8", "CP1252//IGNORE", $cert_fingerprint);

    $response_signature_data = $saml_response->getSignatureData();
    if (\Drupal::config('miniorange_saml.settings')->get('miniorange_saml_response_signed')) {
      $valid_signature = Utilities::processResponse($acs_url, $cert_fingerprint, $response_signature_data, $saml_response);
      if (!$valid_signature){
        echo 'Invalid Signature in SAML Response';
        exit();
      }
    }

    $assertion_signature_data = current($saml_response->getAssertions())->getSignatureData();
    if (\Drupal::config('miniorange_saml.settings')->get('miniorange_saml_assertion_signed')) {
      $valid_signature = Utilities::processResponse($acs_url, $cert_fingerprint, $assertion_signature_data, $saml_response);
      if (!$valid_signature) {
        echo 'Invalid Signature in SAML Assertion';
         exit();
      }
    }

    Utilities::validateIssuerAndAudience($saml_response, $spEntityId, $issuer, $base_url);

    $attrs = current($saml_response->getAssertions())->getAttributes();
	
    if ($username_attribute != 'NameID') {
      if (array_key_exists($username_attribute, $attrs)) {
        $username = $attrs[$username_attribute][0];
      }
      else {
        // Get NameID value if username attribute doesnt exist in response.
        $username = current(current($saml_response->getAssertions())->getNameId());
      }
    }
    else {
      // Get Name ID value.
      $username = current(current($saml_response->getAssertions())->getNameId());
    }

    // Get Email.
    $email_attribute = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_email_attribute');
    if ($email_attribute == 'NameID' ) {
      $email_value = current(current($saml_response->getAssertions())->getNameId());
    }
    else {
      $email_value = $attrs[$email_attribute][0];
    }

    // Get RelayState if any.
	$relay_state = $base_url;
	// var_dump($relay_state); exit;
    if(array_key_exists('RelayState', $post)) {
      if($post['RelayState'] == 'testValidate') {
        $this->showTestResults($username, $attrs);
      } else {
		$relay_state = $post['RelayState'];  
	  }
    }
	
	$sessionIndex = current($saml_response->getAssertions())->getSessionIndex();
	$nameId = current(current($saml_response->getAssertions())->getNameId());
	
	/*Custom Attributes*/
	$custom_attribute_values = array();

	foreach($custom_attributes as $key=>$value){
		if(array_key_exists($value, $attrs)){
			$attr_value = $attrs[$value][0];
			$custom_attribute_values[$key] = $attr_value;
		}
	}
	

	/*Custom Roles*/
		
	  $role_attribute = \Drupal::config('miniorange_saml.settings')->get('miniorange_saml_idp_attr1_name');
		
	  for($i=0 ; $i < sizeof($attrs[$role_attribute]) ; $i++) {
				$myrole[$i]=$attrs[$role_attribute][$i];
		}
			  
	$custom_role_values = array();
	for($i=0; $i < sizeof($myrole) ; $i++) {
	
		foreach($custom_roles as $key=>$value){
		
		if(!empty($value) && !is_null($value) && !(strcasecmp($myrole[$i],$value))){

			$result = db_select('role','rid')
			->fields('rid')
			->condition('name', $key,'=')
			->execute()
			->fetchAssoc();
			$role_value = $result['rid'];
			
			$custom_role_values[$role_value] = $key;
		}
	}
	}
	
    $response = array();
    $response['email'] = $email_value;
    $response['username'] = $username;
	$response['NameID'] = $nameId;
	$response['sessionIndex'] = $sessionIndex;
	$response['customFieldAttributes'] = $custom_attribute_values;
	$response['customFieldRoles'] = $custom_role_values;
	
	if(!empty($relay_state)) {
		$response['relay_state'] = $relay_state;
	}

    return $response;
  }

  public function showTestResults($username, $attrs) {
    $module_path = drupal_get_path('module', 'miniorange_saml');
	
    echo '<div style="font-family:Calibri;padding:0 3%;">';
    if (!empty($username)) {
      echo '<div style="color: #3c763d;
          background-color: #dff0d8; padding:2%;margin-bottom:20px;text-align:center; border:1px solid #AEDB9A; font-size:18pt;">TEST SUCCESSFUL</div>
          <div style="display:block;text-align:center;margin-bottom:4%;"><img style="width:15%;"src="'. $module_path . '/includes/images/green_check.png"></div>';
    }
    else {
      echo '<div style="color: #a94442;background-color: #f2dede;padding: 15px;margin-bottom: 20px;text-align:center;border:1px solid #E6B3B2;font-size:18pt;">TEST FAILED</div>
          <div style="color: #a94442;font-size:14pt; margin-bottom:20px;">WARNING: Some Attributes Did Not Match.</div>
          <div style="display:block;text-align:center;margin-bottom:4%;"><img style="width:15%;"src="'. $module_path . 'includes/images/wrong.png"></div>';
    }
    echo '<span style="font-size:14pt;"><b>Hello</b>, '.$username.'</span><br/><p style="font-weight:bold;font-size:14pt;margin-left:1%;">ATTRIBUTES RECEIVED:</p>
        <table style="border-collapse:collapse;border-spacing:0; display:table;width:100%; font-size:14pt;background-color:#EDEDED;">
        <tr style="text-align:center;"><td style="font-weight:bold;border:2px solid #949090;padding:2%;">ATTRIBUTE NAME</td><td style="font-weight:bold;padding:2%;border:2px solid #949090; word-wrap:break-word;">ATTRIBUTE VALUE</td></tr>';
    if (!empty($attrs)) {
      echo "<tr><td style='font-weight:bold;border:2px solid #949090;padding:2%;'>NameID</td><td style='padding:2%;border:2px solid #949090; word-wrap:break-word;'>" . $username . "</td></tr>";
      foreach ($attrs as $key => $value) {
        echo "<tr><td style='font-weight:bold;border:2px solid #949090;padding:2%;'>" . $key . "</td><td style='padding:2%;border:2px solid #949090; word-wrap:break-word;'>" . implode("<br/>",$value) . "</td></tr>";
      }
    }  
    else {
      echo "<tr><td style='font-weight:bold;border:2px solid #949090;padding:2%;'>NameID</td><td style='padding:2%;border:2px solid #949090; word-wrap:break-word;'>" . $username . "</td></tr>";
    }
    echo '</table></div>';
    echo '<div style="margin:3%;display:block;text-align:center;"><input style="padding:1%;width:100px;background: #0091CD none repeat scroll 0% 0%;cursor: pointer;font-size:15px;border-width: 1px;border-style: solid;border-radius: 3px;white-space: nowrap;box-sizing: border-box;border-color: #0073AA;box-shadow: 0px 1px 0px rgba(120, 200, 230, 0.6) inset;color: #FFF;"type="button" value="Done" onClick="self.close();"></div>';
    exit;
  }

}
