import numpy as np
import re

# import pandas as pd
# import torch
# from torchmetrics.classification.accuracy import BinaryAccuracy


# def train(
#     model: torch.nn.Module,
#     train_dataset,
#     optimizer,
#     loss_fn,
#     metric_fn,
#     epochs: int = 50,
#     batch_size: int = 64,
# ):
#     """train a Pytorch module on a training dataset"""
#     # create a dataloader
#     dataloader = torch.utils.data.DataLoader(
#         train_dataset,
#         batch_size=batch_size,
#         shuffle=True,
#     )
#     # create a loss function
#     # loss_fn = torch.nn.MSELoss()
#     batch_losses, epoch_losses = [], []
#     batch_metrics, epoch_metrics = [], []

#     for epoch in range(epochs):
#         model.train()
#         batch_losses.clear()
#         batch_metrics.clear()
#         for batch in dataloader:
#             # unpack the batch
#             x, y = batch
#             # run the model
#             y_pred = model(x)
#             # calculate the loss
#             batch_loss = loss_fn(y_pred, y)
#             batch_metric = metric_fn(y_pred, y)
#             # store the loss and accuracy
#             batch_losses.append(batch_loss)
#             batch_metrics.append(batch_metric)
#             # calculate the gradients
#             batch_loss.backward()
#             # update the parameters
#             optimizer.step()
#         # calculate average batch loss & metric
#         epoch_loss = torch.mean(torch.tensor(batch_losses))
#         epoch_metric = torch.mean(torch.tensor(batch_metrics))
#         # store the loss and accuracy
#         epoch_losses.append(epoch_loss)
#         epoch_metrics.append(epoch_metric)
#         # print the loss and accuracy
#         print(f"Epoch: {epoch+1:02} | Loss: {epoch_loss:.2f} | Accuracy: {epoch_metric:.2f}")

#     hist = {
#         "epoch_loss": epoch_losses,
#         "epoch_metric": epoch_metrics,
#     }
#     return hist


def validate_email(email) -> bool:
    """Validate email address using regex"""
    regex = r"^[a-zA-Z0-9_+-]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    if re.search(regex, email):
        print(f"{email} is valid.")
        return True
    else:
        print(f"{email} is not a valid email address.")
        return False


def main():
    a = np.array([])
    for i in range(1, 6):
        b = np.arange(i, i + 2)
        a = np.append(a, b)
        print(f"Intermediate: {a}")
    print(f"Final: {a}")
    print(validate_email("anu2cool.sb_abd@abc.com"))
    print(validate_email("anu2cool.sb_abd$#,abc.com"))


if __name__ == "__main__":
    main()
