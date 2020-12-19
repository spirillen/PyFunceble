"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the configuration comparision interface.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import copy
from typing import List, Optional

from PyFunceble.helpers.dict import DictHelper
from PyFunceble.helpers.merge import Merge


class ConfigComparison:
    """
    Provides an interface for comparing 2 configuration.
    """

    DELETED_LINKS: List[str] = [
        "config",
        "dir_structure",
        "iana",
        "ipv4_reputation",
        "mariadb",
        "mysql",
        "psl",
        "repo",
        "requirements",
    ]
    DELETED_CORE: List[str] = [
        "dns_lookup_over_tcp",
        "generate_json",
        "header_printed",
        "iana_whois_server",
        "idna_conversion",
        "maximal_processes",
        "outputs",
        "status",
    ]

    OLD_TO_NEW: dict = {
        "adblock": "cli_decoding.adblock",
        "aggressive": "cli_decoding.adblock_aggressive",
        "auto_continue": "cli_testing.autocontinue",
        "command": "cli_testing.ci.command",
        "command_before_end": "cli_testing.ci.end_command",
        "cooldown_time": "cli_testing.cooldown_time",
        "custom_ip": "cli_testing.hosts_ip",
        "days_between_inactive_db_clean": "cli_testing.days_between.db_clean",
        "days_between_db_retest": "cli_testing.days_between.db_retest",
        "db_type": "cli_testing.db_type",
        "debug": "debug.active",
        "dns_server": "dns.server",
        "filter": "cli_testing.file_filter",
        "generate_complements": "cli_testing.complements",
        "generate_hosts": "cli_testing.file_generation.hosts",
        "hierarchical_sorting": "cli_testing.sorting_mode.hierarchical",
        "inactive_database": "cli_testing.inactive_db",
        "less": "cli_testing.display_mode.less",
        "local": "cli_testing.local_network",
        "mining": "cli_testing.mining",
        "no_files": "cli_testing.file_generation.no_file",
        "plain_list_domain": "cli_testing.file_generation.plain",
        "print_dots": "cli_testing.display_mode.dots",
        "quiet": "cli_testing.display_mode.dots",
        "use_reputation_data": "lookup.reputation",
        "reputation": "lookup.reputation",
        "rpz": "cli_decoding.rpz",
        "show_execution_time": "cli_testing.display_mode.execution_time",
        "show_percentage": "cli_testing.display_mode.percentage",
        "simple": "cli_testing.display_mode.simple",
        "syntax": "cli_testing.testing_mode.syntax",
        "timeout": "lookup.timeout",
        "ci": "cli_testing.ci.active",
        "ci_autosave_commit": "cli_testing.ci.commit_message",
        "ci_autosave_final_commit": "cli_testing.ci.end_commit_message",
        "ci_autosave_minutes": "cli_testing.ci.max_exec_minutes",
        "ci_branch": "cli_testing.ci.branch",
        "ci_distribution_branch": "cli_testing.ci.distribution_branch",
        "whois_database": "cli_testing.whois_db",
        "wildcard": "cli_decoding.wildcard",
    }

    OLD_TO_NEW_NEGATE: dict = {
        "no_special": "lookup.special",
        "no_whois": "lookup.whois",
        "split": "cli_testing.file_generation.unified_results",
    }

    _local_config: dict = dict()
    _upsteam_config: dict = dict()

    dict_helper: DictHelper = DictHelper()

    def __init__(
        self,
        *,
        local_config: Optional[dict] = None,
        upstream_config: Optional[dict] = None,
    ) -> None:
        if local_config:
            self.local_config = local_config

        if upstream_config:
            self.upstream_config = upstream_config

    @property
    def local_config(self) -> dict:
        """
        Provides the current state of the :code:`_local_config`.
        """

        return self._local_config

    @local_config.setter
    def local_config(self, value: dict) -> None:
        """
        Sets the local configuration to work with.

        :raise TypeError:
            When :code:`value` is not a :py:class:`dict`.
        """

        if not isinstance(value, dict):
            raise TypeError(f"<value> should be {dict}, {type(value)} given.")

        self._local_config = copy.deepcopy(value)

    def set_local_config(self, value: dict) -> "ConfigComparison":
        """
        Sets the local configuration to work with.
        """

        self.local_config = value

        return self

    @property
    def upstream_config(self) -> dict:
        """
        Provides the current state of the :code:`_upstream_config`.
        """

        return self._upsteam_config

    @upstream_config.setter
    def upstream_config(self, value: dict) -> None:
        """
        Sets the upstram configuration to work with.

        :raise TypeError:
            When :code:`value` is not a :py:class:`dict`
        """

        if not isinstance(value, dict):
            raise TypeError(f"<value> should be {dict}, {type(value)} given.")

        self._upsteam_config = copy.deepcopy(value)

    def set_upstream_config(self, value: dict) -> "ConfigComparison":
        """
        Sets the upstram configuration to work with.
        """

        self.upstream_config = value

        return self

    def is_local_identical(self) -> bool:
        """
        Checks if the local configuration is identical to the upstream one.
        """

        # pylint: disable=too-many-boolean-expressions
        if (
            not self.dict_helper.set_subject(self.local_config).has_same_keys_as(
                self.upstream_config
            )
            or "user_agent" not in self.local_config
            or not isinstance(self.local_config["user_agent"], dict)
            or "active" in self.local_config["http_codes"]
        ):
            return False

        for index in self.local_config:
            if index in self.DELETED_CORE:
                return False

        for index in self.local_config["links"]:
            if index in self.DELETED_LINKS:
                return False

        return True

    def get_merged(self) -> dict:
        """
        Provides the merged configuration.
        """

        # pylint: disable=too-many-branches

        if not self.is_local_identical():

            merged_original = Merge(self.upstream_config).into(self.local_config)
            merged = copy.deepcopy(merged_original)

            flatten_merged = self.dict_helper.set_subject(merged).flatten()

            for key, value in self.OLD_TO_NEW.items():
                if key not in flatten_merged:
                    continue

                if value not in flatten_merged:
                    raise RuntimeError(f"<value> {value!r} not found.")

                flatten_merged[value] = merged[key]

                del flatten_merged[key]

            for key, value in self.OLD_TO_NEW_NEGATE.items():
                if key not in flatten_merged:
                    continue

                if value not in flatten_merged:
                    raise RuntimeError(f"<value> {value!r} not found.")

                flatten_merged[value] = not merged[key]

                del flatten_merged[key]

            merged = self.dict_helper.set_subject(flatten_merged).unflatten()
            del flatten_merged

            if "dns_lookup_over_tcp" in merged and merged["dns_lookup_over_tcp"]:
                merged["dns_protocol"] = "TCP"

            if merged["cli_testing"]["db_type"] == "json":
                merged["cli_testing"]["db_type"] = "csv"

            if merged["cli_testing"]["cooldown_time"] is None:
                merged["cli_testing"]["cooldown_time"] = copy.deepcopy(
                    self.upstream_config["cli_testing"]["cooldown_time"]
                )

            for index in self.DELETED_CORE:
                if index in merged:
                    del merged[index]

            for index in self.DELETED_LINKS:
                if index in merged["links"]:
                    del merged["links"][index]

            if not isinstance(self.local_config["user_agent"], dict):
                merged["user_agent"] = self.upstream_config["user_agent"]

            if "active" in merged["http_codes"]:
                merged["no_http_codes"] = not merged["http_codes"]["active"]

                del merged["http_codes"]["active"]

            return merged
        return self.local_config