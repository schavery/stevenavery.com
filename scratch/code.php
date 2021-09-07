<?php
	$file = file_get_contents('addresses.csv');
	$file = explode("\n", $file);
	foreach($file as &$row) {
		if(strlen($row) > 0) {
			$addr = explode(',', $row);
			$base_url = 'https://maps.googleapis.com/maps/api/geocode/json?';
			$base_url .= 'address=' . str_replace(' ', '+', $addr[1]);
			$base_url .= ',+' . str_replace(' ', '+', $addr[2]);
			$base_url .= ',+' . $addr[3] . '+' . $addr[4];
			$base_url .= '&key=AIzaSyChnads-VRGDmGdzGsCr-CDCk2FajVIX40';

			$response = json_decode(file_get_contents($base_url));
			if($response->status == 'OK') {
				$addr[] = $response->results[0]->geometry->location->lat;
				$addr[] = $response->results[0]->geometry->location->lng;
			} else {
				echo "\t\t\t Error: " . $response->error_message;
			}

			$row = implode(',', $addr);
		}
	}

	file_put_contents('addresses_coded.csv', implode("\n", $file));
