        def resolve_acls():
            """Resolve ACL references in config."""

            def build_acl(acl, vid=None):
                """Check that ACL can be built from config."""
                if acl.rules:
                    assert valve_acl.build_acl_ofmsgs(
                        [acl], self.wildcard_table,
                        valve_of.goto_table(self.wildcard_table),
                        2**16, self.meters, acl.exact_match,
                        vlan_vid=vid)

            for vlan in list(self.vlans.values()):
                if vlan.acl_in:
                    if vlan.acl_in in self.acls:
                        vlan.acl_in = self.acls[vlan.acl_in]
                        build_acl(vlan.acl_in, vid=1)
                    else:
                        assert False, 'Unconfigured vlan for %s' % self.name
            for port in list(self.ports.values()):
                if port.acl_in:
                    if port.acl_in in self.acls:
                        port.acl_in = self.acls[port.acl_in]
                        build_acl(port.acl_in)
                    else:
                        assert False, 'Unconfigured acl for %s' % self.name