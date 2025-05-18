# secsec360: Xbox 360 security sector dumper

Stupid Sunday project. This time, it's a tool to dump the security sectors on Xbox 360 hard drives.

## Usage

`sudo python3 secsec360 /dev/diskX`

This will write your security sector into the appropriate folder in `dumps/`.

## How are the dumps useful?

They aren't. Microsoft secured the hard drives with an RSA-2048 signature so as to prevent third party
hard drives. The obvious reason for this is money: the Xbox console line has always been a money pit for
Microsoft, and they sell the consoles at a loss, so they have to make the money back somehow through
peripherals and Xbox Live subscriptions.

That said, the dumps are provided here mainly for historical interest, and in case one day someone figures
out how to generate hash collisions faster than a glacial pace. (I have too many 360 hard drives lying around
and wanted to back up the sectors.)

## Got dumps?

If you want to add your dump to the database, run the tool to dump your security sector and open a pull request.
I'd think there's a database for these things already, but I guess it doesn't hurt to have another.

## Further reading

- [Eaton's writeup about the security sector](https://eaton-works.com/2023/01/24/how-the-xbox-360-knows-if-your-hard-drive-is-genuine/)

## License

Public domain
