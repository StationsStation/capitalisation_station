
# Apprise Connection

## Description

This is a connection to send notifications using the [Apprise](https://pypi.org/project/apprise/) library. 

This connection is used to send notifications to a user using the Apprise library. The user can be notified via various services such as email, SMS, Slack, Discord, etc.

## Example Configuration

```yaml
config:
  endpoints:
  - ntfy://ntfy.sh/8baller
```

In order to use other endpoints, all that is necessary is to change the URL in the `endpoints` list.

To Send notifications, the agent simply needs to send a notification message to the connection.

```python
from packages.eightballer.connections.apprise_wrapper.connection import (
    CONNECTION_ID as APPRISE_PUBLIC_ID,
)
from packages.eightballer.protocols.user_interaction.dialogues import (
    UserInteractionDialogues,
)
from packages.eightballer.protocols.user_interaction.message import (
    UserInteractionMessage,
)


class Behaviour(Behaviour):
    """This class defines a behaviour."""

    def send_notification_to_user(
        self, title: str, msg: str, attach: str = None
    ) -> None:
        """Send notification to user."""
        dialogues = cast(
            UserInteractionDialogues, self.context.user_interaction_dialogues
        )
        msg, _ = dialogues.create(
            counterparty=str(APPRISE_PUBLIC_ID),
            performative=UserInteractionMessage.Performative.NOTIFICATION,
            title=title,
            body=msg,
            attach=attach,
        )
        self.context.outbox.put_message(message=msg)

```
