// Licensed to Elasticsearch B.V. under one or more contributor
// license agreements. See the NOTICE file distributed with
// this work for additional information regarding copyright
// ownership. Elasticsearch B.V. licenses this file to you under
// the Apache License, Version 2.0 (the "License"); you may
// not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.

// Code generated by beats/dev-tools/cmd/asset/asset.go - DO NOT EDIT.

package collectd

import (
	"github.com/elastic/beats/v7/libbeat/asset"
)

func init() {
	if err := asset.SetFields("filebeat", "collectd", asset.ModuleFieldsPri, AssetCollectd); err != nil {
		panic(err)
	}
}

// AssetCollectd returns asset data.
// This is the base64 encoded gzipped contents of module/collectd.
func AssetCollectd() string {
	return "eJyk0bFuuzAQx/Gdp/iJPXkA1v/83yJ1rFz7gFNsH+IujejTV6FOCpS2QxnP9vc+EgecaWrgJUbyFirA2CI1qO+jugICqR95MJa8OMF/CZdItwstUwzaVABwQHaJVs3bZ9NADbpRLkOZfFON0mldriy7y7aaMw2P8V7964Z/ks1x1lJFO0p6KEty3n6sF40tYck407Sa3x1nmq4yhs3ZWnPqaa5AWlhP835WYw+noMRmFPAyFdeK9Al4dfFCu4Q2irNfAfP7PwmME6m5NDwreclBdzVRcvcj5qmnvEFcnWIkL13mtw/I/V8dceJEUM6e5kc0iO/BGcVwrKvqPQAA//95d9aj"
}
