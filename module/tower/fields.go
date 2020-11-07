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

package tower

import (
	"github.com/elastic/beats/v7/libbeat/asset"
)

func init() {
	if err := asset.SetFields("filebeat", "tower", asset.ModuleFieldsPri, AssetTower); err != nil {
		panic(err)
	}
}

// AssetTower returns asset data.
// This is the base64 encoded gzipped contents of module/tower.
func AssetTower() string {
	return "eJy8kEEOwiAURPecYtJ9L8DCG5h4BSIjIdJCCtX29kaslqY10YUuGR7zH7/GmaNE8ld2Akg2OUpU+VwJQDMeOxuS9a3ETgB4sNh73TsK4GTpdJT5qkarGs51GR8DJUzn+zAlG53LmndVq8cHRxUJpXWZFzQH1YT7jwpyygpqrbhlNDs5XuiK/FurT71e87wxiyX8emDDGJXhHyY+l584JHELAAD//x70uqc="
}
