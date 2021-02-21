"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the domains availability checker.

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


    Copyright 2017, 2018, 2019, 2020, 2021 Nissar Chababy

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


import PyFunceble.facility
import PyFunceble.factory
import PyFunceble.storage
from PyFunceble.checker.availability.base import AvailabilityCheckerBase
from PyFunceble.checker.availability.extra_rules import ExtraRulesHandler
from PyFunceble.checker.reputation.domain import DomainReputationChecker


class DomainAvailabilityChecker(AvailabilityCheckerBase):
    """
    Provides the interface for checking the availability of a given domain.
    """

    def try_to_query_status_from_reputation(self) -> "DomainAvailabilityChecker":
        """
        Tries to query the status from the reputation lookup.
        """

        PyFunceble.facility.Logger.info(
            "Started to try to query the status of %r from: Reputation Lookup",
            self.status.idna_subject,
        )

        lookup_result = DomainReputationChecker(self.status.idna_subject).get_status()

        # pylint: disable=no-member
        if lookup_result and lookup_result.is_malicious():
            self.status.status = PyFunceble.storage.STATUS.up
            self.status.status_source = "REPUTATION"

            PyFunceble.facility.Logger.info(
                "Could define the status of %r from: Reputation Lookup",
                self.status.idna_subject,
            )

        PyFunceble.facility.Logger.info(
            "Finished to try to query the status of %r from: Reputation Lookup",
            self.status.idna_subject,
        )

        return self

    @AvailabilityCheckerBase.ensure_subject_is_given
    @AvailabilityCheckerBase.update_status_date_after_query
    def query_status(self) -> "DomainAvailabilityChecker":
        """
        Queries the result without anything more.
        """

        status_post_syntax_checker = None

        if not self.status.status and self.do_syntax_check_first:
            self.try_to_query_status_from_syntax_lookup()

            if self.status.status:
                status_post_syntax_checker = self.status.status

        if (
            self.should_we_continue_test(status_post_syntax_checker)
            and self.status.second_level_domain_syntax
            and self.use_whois_lookup
        ):
            self.try_to_query_status_from_whois()

        if (
            self.should_we_continue_test(status_post_syntax_checker)
            and self.use_dns_lookup
        ):
            self.try_to_query_status_from_dns()

        if (
            self.should_we_continue_test(status_post_syntax_checker)
            and self.use_netinfo_lookup
        ):
            self.try_to_query_status_from_netinfo()

        if (
            self.should_we_continue_test(status_post_syntax_checker)
            and self.use_reputation_lookup
        ):
            self.try_to_query_status_from_reputation()

        if (
            self.should_we_continue_test(status_post_syntax_checker)
            and self.use_http_code_lookup
        ):
            self.try_to_query_status_from_http_status_code()

        if not self.status.status:
            self.status.status = PyFunceble.storage.STATUS.down
            self.status.status_source = "STDLOOKUP"

            PyFunceble.facility.Logger.info(
                "Could not define status the status of %r. Setting to %r",
                self.status.idna_subject,
                self.status.status,
            )

        if self.use_extra_rules:
            ExtraRulesHandler(self.status).start()

        return self

    @staticmethod
    def is_valid() -> bool:
        raise NotImplementedError()
