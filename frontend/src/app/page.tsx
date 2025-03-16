'use client';

import { useState } from 'react';
import {
  Container,
  VStack,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
} from '@chakra-ui/react';
import { TeamSelector } from '../components/TeamSelector';
import { PlayerList } from '../components/PlayerList';
import StatsViewer from '../components/StatsViewer';

export default function Home() {
  const [selectedTeam, setSelectedTeam] = useState<string | null>(null);

  return (
    <Container maxW="container.xl" py={8}>
      <VStack spacing={8} align="stretch">
        <Tabs>
          <TabList>
            <Tab>チーム/選手</Tab>
            <Tab>成績</Tab>
          </TabList>
          <TabPanels>
            <TabPanel>
              <VStack spacing={8} align="stretch">
                <TeamSelector onTeamSelect={setSelectedTeam} />
                <PlayerList teamId={selectedTeam} />
              </VStack>
            </TabPanel>
            <TabPanel>
              <StatsViewer />
            </TabPanel>
          </TabPanels>
        </Tabs>
      </VStack>
    </Container>
  );
}