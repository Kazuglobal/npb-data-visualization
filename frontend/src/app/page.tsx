'use client';

import { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Heading,
  Text,
  VStack,
  SimpleGrid,
  useColorModeValue,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
} from '@chakra-ui/react';
import { TeamSelector } from '../components/TeamSelector';
import { PlayerList } from '../components/PlayerList';
import { Statistics } from '../components/Statistics';

export default function Home() {
  const [selectedTeam, setSelectedTeam] = useState<string | null>(null);
  const bgColor = useColorModeValue('white', 'gray.800');

  return (
    <Container maxW="container.xl" py={8}>
      <VStack spacing={8} align="stretch">
        <Box>
          <Heading as="h1" size="2xl" mb={2}>
            NPB選手データ
          </Heading>
          <Text color="gray.600">
            日本のプロ野球選手の最新情報をチェック
          </Text>
        </Box>

        <Statistics />

        <Tabs variant="enclosed">
          <TabList>
            <Tab>チーム選択</Tab>
            <Tab>選手一覧</Tab>
          </TabList>

          <TabPanels>
            <TabPanel>
              <TeamSelector onSelectTeam={setSelectedTeam} selectedTeam={selectedTeam} />
            </TabPanel>
            <TabPanel>
              <PlayerList teamId={selectedTeam} />
            </TabPanel>
          </TabPanels>
        </Tabs>
      </VStack>
    </Container>
  );
}