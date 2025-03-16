import { useState } from 'react';
import {
  Box,
  Container,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
} from '@chakra-ui/react';
import TeamSelector from '../components/TeamSelector';
import PlayerList from '../components/PlayerList';
import StatsViewer from '../components/StatsViewer';
import TeamInfo from '../components/TeamInfo';

export default function Home() {
  const [selectedTeam, setSelectedTeam] = useState<string | null>(null);

  return (
    <Container maxW="container.xl" py={8}>
      <Tabs>
        <TabList>
          <Tab>チーム/選手</Tab>
          <Tab>チーム情報</Tab>
          <Tab>統計情報</Tab>
        </TabList>

        <TabPanels>
          <TabPanel>
            <Box mb={6}>
              <TeamSelector onTeamSelect={setSelectedTeam} />
            </Box>
            {selectedTeam && <PlayerList teamId={selectedTeam} />}
          </TabPanel>

          <TabPanel>
            <TeamInfo />
          </TabPanel>

          <TabPanel>
            <StatsViewer />
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Container>
  );
}