have to add new fields to the model: JDMatchDtl
"""
{
role
company
analyzed on
}
"""

update the apis accordingly.

- according to the new design in Node ID: gJbsB, figure out that if it's a jd text or jd-url (write the logic or if it already exist don't)
- the company select is basically selectable + addable select. i.e.
  > user can select from the existing list of companies or can add a new company.
  > that company needs to be saved in the backend, in a separate table. when new user comes, user can see that new company, added by previous user (in the list).

using pencil.design mcp, revamp the ui taking the reference from Node ID: 9ZRAq
