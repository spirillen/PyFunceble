"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the interface for the MariaDB management.

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

import PyFunceble.cli.factory
from PyFunceble.database.sqlalchemy.all_schemas import Continue
from PyFunceble.dataset.autocontinue.base import ContinueDatasetBase
from PyFunceble.dataset.mariadb_base import MariaDBDatasetBase


class MariaDBContinueDataset(MariaDBDatasetBase, ContinueDatasetBase):
    """
    Provides the interface for the management and the Continue dataset unser
    mariadb.
    """

    ORM_OBJ: Continue = Continue

    @MariaDBDatasetBase.execute_if_authorized(None)
    @MariaDBDatasetBase.handle_db_session
    # pylint: disable=arguments-differ
    def cleanup(self, *, session_id: str) -> "MariaDBContinueDataset":
        """
        Cleanups the dataset. Meaning that we delete every entries which are
        needed anymore.

        :param source:
            The source to delete.
        :param destination:
            The destination to delete.
        :param checker_type:
            The checker type to delete.
        :param session_id:
            The session ID to cleanup.
        """

        self.db_session.query(self.ORM_OBJ).filter(
            self.ORM_OBJ.session_id == session_id
        ).delete(synchronize_session=False)
        self.db_session.commit()

        PyFunceble.facility.Logger.debug(
            "Deleted data related to %s (session_id", session_id
        )

        return self
